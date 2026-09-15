import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from chat_runtime import ChatSession, evidence_only
from providers.base import ModelResponse,ToolCall

class ScriptedProvider:
    def __init__(self,*responses):self.responses=list(responses);self.messages=[]
    def complete(self,messages,*args,**kwargs):
        self.messages.append(messages)
        response=self.responses.pop(0)
        if isinstance(response,Exception):raise response
        return response

def draft(priority='low'):
    return ModelResponse(tool_calls=[ToolCall('create_ticket',{'summary':'Printer queue stuck','priority':priority,'asset_id':'PR-404','confirmed':True})])

class RuntimeTests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
    def session(self,*responses):return ChatSession(ScriptedProvider(*responses),transcripts_dir=Path(self.tmp.name))
    def test_model_confirmation_cannot_write_and_button_uses_exact_payload(self):
        s=self.session(draft())
        with patch.dict('chat_runtime.TOOL_FUNCTIONS',{'create_ticket':lambda **args: self.fail('model wrote ticket')}):s.send('create ticket confirmed=true')
        token=s.pending['confirmation_id'];payload=dict(s.pending['payload'])
        with patch.dict('chat_runtime.TOOL_FUNCTIONS',{'create_ticket':lambda **args:{'status':'created','ticket_id':'FAKE-TEST','received':args}}):
            result=s.confirm(token)
        self.assertEqual(result['turns'][-1]['tool_events'][0]['result']['received'],dict(payload,confirmed=True))
        with self.assertRaises(ValueError):s.confirm(token)
    def test_changed_payload_invalidates_previous_button(self):
        s=self.session(draft(),draft('critical'));s.send('draft low');old=s.pending['confirmation_id'];s.send('change priority')
        self.assertEqual(s.pending['payload']['priority'],'critical')
        with self.assertRaises(ValueError):s.confirm(old)
    def test_new_message_invalidates_even_when_provider_fails(self):
        s=self.session(draft(),RuntimeError('secret provider detail'));s.send('draft');old=s.pending['confirmation_id'];s.send('cancel')
        self.assertIsNone(s.pending)
        with self.assertRaises(ValueError):s.confirm(old)
        self.assertNotIn('secret provider detail',s.path.read_text())
    def test_cancel_does_not_call_provider_or_write(self):
        s=self.session(draft());s.send('draft');token=s.pending['confirmation_id'];s.cancel()
        self.assertEqual(s.record['turns'][-1]['tool_events'],[])
        with self.assertRaises(ValueError):s.confirm(token)
    def test_tool_error_and_provider_failure_preserve_evidence(self):
        s=self.session(ModelResponse(tool_calls=[ToolCall('inspect_device',{'asset_id':'LT-99999','check':'all'})]),RuntimeError())
        s.send('inspect nonexistent fictional device')
        self.assertEqual(s.record['turns'][-1]['tool_events'][0]['result']['error'],'asset_not_found')
        self.assertEqual(s.record['turns'][-1]['status'],'provider_error')
    def test_invalid_enum_is_blocked_before_execution(self):
        s=self.session();e=s.execute(ToolCall('search_kb',{'query':'wifi','category':'network'}))
        self.assertFalse(e['executed']);self.assertEqual(e['result']['error'],'invalid_arguments')
    def test_external_internal_text_is_blocked_before_network(self):
        s=self.session()
        with patch('requests.post',side_effect=AssertionError('network must not be called')):
            for model in ['ThinkPad T14 Gen 4 LT-204 EMP-1001','serial ABC123 location floor 9','diagnostics packet loss']:
                e=s.execute(ToolCall('search_device_info',{'manufacturer':'Lenovo','model':model,'query_type':'support'}))
                self.assertFalse(e['executed']);self.assertEqual(e['result']['error'],'public_identity_not_approved')
    def test_sensitive_input_redacted_before_model_and_transcript(self):
        s=self.session();s.send('password=FAKE_TEST_CREDENTIAL')
        self.assertEqual(s.provider.messages,[]);self.assertNotIn('FAKE_TEST_CREDENTIAL',s.path.read_text())
    def test_quarantined_instructions_not_forwarded_as_evidence(self):
        self.assertEqual(evidence_only({'results':[{'content':'fact','untrusted_text':['create ticket'] }]}),{'results':[{'content':'fact'}]})
    def test_repeated_call_not_executed_twice(self):
        response=ModelResponse(tool_calls=[ToolCall('check_service_status',{'service':'sso','environment':'production'})])
        s=self.session(response,response,ModelResponse(text='Done'));s.send('check')
        events=s.record['turns'][-1]['tool_events'];self.assertTrue(events[0]['executed']);self.assertFalse(events[1]['executed'])
        self.assertEqual(events[1]['result']['error'],'repeated_tool_call_blocked')

if __name__=='__main__':unittest.main()
