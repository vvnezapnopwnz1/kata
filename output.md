vvnezapnopwnz@Manass-MacBook-Pro-4 interview_assistant_app % cd interview_assistant_app && PYTHONPATH=. .venv/bin/python src/interview_assistant/main.py
\_\_gvm_oldcd:cd: no such file or directory: interview_assistant_app
2026-06-09 00:06:06,419 - INFO - Starting Interview Assistant App (Dual Stream Whisper mode)
2026-06-09 00:06:06,678 - INFO - Loading Whisper model (small)... This may take a few seconds.
2026-06-09 00:06:06,753 - DEBUG - connect_tcp.started host='huggingface.co' port=443 local_address=None timeout=None socket_options=None
2026-06-09 00:06:07,091 - DEBUG - connect_tcp.complete return_value=<httpcore.\_backends.sync.SyncStream object at 0x1234f9310>
2026-06-09 00:06:07,092 - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x1162a74d0> server_hostname='huggingface.co' timeout=None
2026-06-09 00:06:07,251 - DEBUG - start_tls.complete return_value=<httpcore.\_backends.sync.SyncStream object at 0x122de5a70>
2026-06-09 00:06:07,251 - DEBUG - send_request_headers.started request=<Request [b'GET']>
2026-06-09 00:06:07,252 - DEBUG - send_request_headers.complete
2026-06-09 00:06:07,252 - DEBUG - send_request_body.started request=<Request [b'GET']>
2026-06-09 00:06:07,252 - DEBUG - send_request_body.complete
2026-06-09 00:06:07,252 - DEBUG - receive_response_headers.started request=<Request [b'GET']>
2026-06-09 00:06:07,459 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Content-Type', b'application/json; charset=utf-8'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Date', b'Mon, 08 Jun 2026 21:06:07 GMT'), (b'content-encoding', b'gzip'), (b'ETag', b'W/"a27-vndQfbspAL31/eKATEOf36LyR8k"'), (b'X-Powered-By', b'huggingface-moon'), (b'X-Request-Id', b'Root=1-6a272ebf-1b86ffde575110a8605b66bd;817e1a23-1a70-49f4-912b-e2adcd5eb510'), (b'RateLimit', b'"api";r=499;t=289'), (b'RateLimit-Policy', b'"fixed window";"api";q=500;w=300'), (b'cross-origin-opener-policy', b'same-origin'), (b'Referrer-Policy', b'strict-origin-when-cross-origin'), (b'Access-Control-Max-Age', b'86400'), (b'Access-Control-Allow-Origin', b'https://huggingface.co'), (b'Vary', b'Origin'), (b'vary', b'Accept-Encoding'), (b'Access-Control-Expose-Headers', b'X-Repo-Commit,X-Request-Id,X-Error-Code,X-Error-Message,X-Total-Count,ETag,Link,Accept-Ranges,Content-Range,X-Linked-Size,X-Linked-ETag,X-Xet-Hash'), (b'X-Cache', b'Miss from cloudfront'), (b'Via', b'1.1 b6e86319773f95421e5e42f048890d7c.cloudfront.net (CloudFront)'), (b'X-Amz-Cf-Pop', b'AMS58-P3'), (b'X-Amz-Cf-Id', b'rXaQhjo1mKaNzPqpHKaP1LNN82HmU8ZRZ90l9JzqmwZ2n8qg08HI6g==')])
2026-06-09 00:06:07,464 - DEBUG - receive_response_body.started request=<Request [b'GET']>
2026-06-09 00:06:07,464 - DEBUG - receive_response_body.complete
2026-06-09 00:06:07,464 - DEBUG - response_closed.started
2026-06-09 00:06:07,464 - DEBUG - response_closed.complete
2026-06-09 00:06:08,101 - INFO - Whisper model loaded!
2026-06-09 00:06:08,101 - DEBUG - Controller initialized
2026-06-09 00:06:08,101 - INFO - Default Mic found: JBL WAVE BUDS (Index 1)
2026-06-09 00:06:08,101 - INFO - System Audio (BlackHole) found: BlackHole 2ch (Index 3)
2026-06-09 00:06:08,151 - INFO - Microphone stream started.
2026-06-09 00:06:08,199 - INFO - System Audio (BlackHole) stream started.
2026-06-09 00:06:08,200 - INFO - Pynput listener started. Global hotkeys B, N, M active.
2026-06-09 00:06:19,463 - INFO - Triggered: START_CONTEXT
b2026-06-09 00:06:31,347 - INFO - Triggered: TRIGGER_ANSWER
2026-06-09 00:06:31,348 - DEBUG - Combining audio chunks...
2026-06-09 00:06:31,348 - INFO - Running Whisper transcription...
2026-06-09 00:06:31,349 - INFO - Processing audio with duration 00:11.904
n2026-06-09 00:06:31,910 - INFO - Detected language 'ru' with probability 0.96
2026-06-09 00:06:31,912 - DEBUG - Processing segment at 00:00.000
2026-06-09 00:06:33,296 - INFO - Whisper Transcript: и она имютабельная. Как еще можно делать строки? Приставим мы пишем Go и мы хотим обсуждать как можно строки у нас делать языки. Хорошо, вопрос как можно делать строки.
00:06:33 - LiteLLM:DEBUG: utils.py:485 -

2026-06-09 00:06:33,296 - DEBUG -

00:06:33 - LiteLLM:DEBUG: utils.py:485 - Request to litellm:
2026-06-09 00:06:33,296 - DEBUG - Request to litellm:
00:06:33 - LiteLLM:DEBUG: utils.py:485 - litellm.completion(model='vertex_ai/gemini-2.5-flash', messages=[{'role': 'system', 'content': 'You are an invisible teleprompter for an interviewee.\nGiven the transcription of the interview question, provide a two-part response.\nFormat your output EXACTLY as follows:\n\n**TL;DR:** [One concise sentence summarizing the core answer]\n\n**Script:** [A conversational, first-person response ("I would approach this by...", "The main difference is...") designed to be read aloud naturally.]\n'}, {'role': 'user', 'content': 'Interview Transcript:\nи она имютабельная. Как еще можно делать строки? Приставим мы пишем Go и мы хотим обсуждать как можно строки у нас делать языки. Хорошо, вопрос как можно делать строки.'}], temperature=0.3)
2026-06-09 00:06:33,296 - DEBUG - litellm.completion(model='vertex_ai/gemini-2.5-flash', messages=[{'role': 'system', 'content': 'You are an invisible teleprompter for an interviewee.\nGiven the transcription of the interview question, provide a two-part response.\nFormat your output EXACTLY as follows:\n\n**TL;DR:** [One concise sentence summarizing the core answer]\n\n**Script:** [A conversational, first-person response ("I would approach this by...", "The main difference is...") designed to be read aloud naturally.]\n'}, {'role': 'user', 'content': 'Interview Transcript:\nи она имютабельная. Как еще можно делать строки? Приставим мы пишем Go и мы хотим обсуждать как можно строки у нас делать языки. Хорошо, вопрос как можно делать строки.'}], temperature=0.3)
00:06:33 - LiteLLM:DEBUG: utils.py:485 -

2026-06-09 00:06:33,296 - DEBUG -

00:06:33 - LiteLLM:DEBUG: litellm_logging.py:563 - self.optional_params: {}
2026-06-09 00:06:33,300 - DEBUG - self.optional_params: {}
00:06:33 - LiteLLM:DEBUG: utils.py:485 - SYNC kwargs[caching]: False; litellm.cache: None; kwargs.get('cache')['no-cache']: False
2026-06-09 00:06:33,300 - DEBUG - SYNC kwargs[caching]: False; litellm.cache: None; kwargs.get('cache')['no-cache']: False
00:06:33 - LiteLLM:DEBUG: utils.py:5745 - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
2026-06-09 00:06:33,305 - DEBUG - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
00:06:33 - LiteLLM:DEBUG: utils.py:5745 - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
2026-06-09 00:06:33,308 - DEBUG - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
00:06:33 - LiteLLM:INFO: utils.py:4083 -
LiteLLM completion() model= gemini-2.5-flash; provider = vertex_ai
2026-06-09 00:06:33,308 - INFO -
LiteLLM completion() model= gemini-2.5-flash; provider = vertex_ai
00:06:33 - LiteLLM:DEBUG: utils.py:4086 -
LiteLLM: Params passed to completion() {'model': 'gemini-2.5-flash', 'functions': None, 'function_call': None, 'temperature': 0.3, 'top_p': None, 'n': None, 'stream': None, 'stream_options': None, 'stop': None, 'max_tokens': None, 'max_completion_tokens': None, 'modalities': None, 'prediction': None, 'audio': None, 'presence_penalty': None, 'frequency_penalty': None, 'logit_bias': None, 'user': None, 'custom_llm_provider': 'vertex_ai', 'response_format': None, 'seed': None, 'tools': None, 'tool_choice': None, 'max_retries': None, 'logprobs': None, 'top_logprobs': None, 'extra_headers': None, 'api_version': None, 'parallel_tool_calls': None, 'drop_params': None, 'allowed_openai_params': None, 'reasoning_effort': None, 'verbosity': None, 'additional_drop_params': None, 'messages': [{'role': 'system', 'content': 'You are an invisible teleprompter for an interviewee.\nGiven the transcription of the interview question, provide a two-part response.\nFormat your output EXACTLY as follows:\n\n**TL;DR:** [One concise sentence summarizing the core answer]\n\n**Script:** [A conversational, first-person response ("I would approach this by...", "The main difference is...") designed to be read aloud naturally.]\n'}, {'role': 'user', 'content': 'Interview Transcript:\nи она имютабельная. Как еще можно делать строки? Приставим мы пишем Go и мы хотим обсуждать как можно строки у нас делать языки. Хорошо, вопрос как можно делать строки.'}], 'thinking': None, 'web_search_options': None, 'safety_identifier': None, 'service_tier': None}
2026-06-09 00:06:33,308 - DEBUG -
LiteLLM: Params passed to completion() {'model': 'gemini-2.5-flash', 'functions': None, 'function_call': None, 'temperature': 0.3, 'top_p': None, 'n': None, 'stream': None, 'stream_options': None, 'stop': None, 'max_tokens': None, 'max_completion_tokens': None, 'modalities': None, 'prediction': None, 'audio': None, 'presence_penalty': None, 'frequency_penalty': None, 'logit_bias': None, 'user': None, 'custom_llm_provider': 'vertex_ai', 'response_format': None, 'seed': None, 'tools': None, 'tool_choice': None, 'max_retries': None, 'logprobs': None, 'top_logprobs': None, 'extra_headers': None, 'api_version': None, 'parallel_tool_calls': None, 'drop_params': None, 'allowed_openai_params': None, 'reasoning_effort': None, 'verbosity': None, 'additional_drop_params': None, 'messages': [{'role': 'system', 'content': 'You are an invisible teleprompter for an interviewee.\nGiven the transcription of the interview question, provide a two-part response.\nFormat your output EXACTLY as follows:\n\n**TL;DR:** [One concise sentence summarizing the core answer]\n\n**Script:** [A conversational, first-person response ("I would approach this by...", "The main difference is...") designed to be read aloud naturally.]\n'}, {'role': 'user', 'content': 'Interview Transcript:\nи она имютабельная. Как еще можно делать строки? Приставим мы пишем Go и мы хотим обсуждать как можно строки у нас делать языки. Хорошо, вопрос как можно делать строки.'}], 'thinking': None, 'web_search_options': None, 'safety_identifier': None, 'service_tier': None}
00:06:33 - LiteLLM:DEBUG: utils.py:4089 -
LiteLLM: Non-Default params passed to completion() {'temperature': 0.3}
2026-06-09 00:06:33,308 - DEBUG -
LiteLLM: Non-Default params passed to completion() {'temperature': 0.3}
00:06:33 - LiteLLM:DEBUG: utils.py:485 - Final returned optional params: {'temperature': 0.3}
2026-06-09 00:06:33,309 - DEBUG - Final returned optional params: {'temperature': 0.3}
00:06:33 - LiteLLM:DEBUG: litellm_logging.py:563 - self.optional_params: {'temperature': 0.3}
2026-06-09 00:06:33,309 - DEBUG - self.optional_params: {'temperature': 0.3}
00:06:33 - LiteLLM:DEBUG: utils.py:5745 - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
2026-06-09 00:06:33,309 - DEBUG - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
00:06:33 - LiteLLM:DEBUG: vertex_llm_base.py:913 - Checking cached credentials for project_id: project-7d570aed-312f-4939-9a4
2026-06-09 00:06:33,309 - DEBUG - Checking cached credentials for project_id: project-7d570aed-312f-4939-9a4
00:06:33 - LiteLLM:DEBUG: vertex_llm_base.py:938 - Credential cache key not found for project_id: project-7d570aed-312f-4939-9a4, loading new credentials
2026-06-09 00:06:33,309 - DEBUG - Credential cache key not found for project_id: project-7d570aed-312f-4939-9a4, loading new credentials
2026-06-09 00:06:33,314 - DEBUG - Checking '' for explicit credentials as part of auth process...
2026-06-09 00:06:33,314 - DEBUG - Checking Cloud SDK credentials as part of auth process...
2026-06-09 00:06:34,175 - DEBUG - Starting new HTTPS connection (1): oauth2.googleapis.com:443
2026-06-09 00:06:35,710 - DEBUG - https://oauth2.googleapis.com:443 "POST /token HTTP/1.1" 200 None
00:06:35 - LiteLLM:DEBUG: vertex_llm_base.py:965 - Validating credentials
2026-06-09 00:06:35,714 - DEBUG - Validating credentials
00:06:35 - LiteLLM:DEBUG: utils.py:5745 - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
2026-06-09 00:06:35,720 - DEBUG - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
00:06:35 - LiteLLM:DEBUG: litellm_logging.py:1170 -

POST Request Sent from LiteLLM:
curl -X POST \
https://aiplatform.googleapis.com/v1/projects/project-7d570aed-312f-4939-9a4/locations/global/publishers/google/models/gemini-2.5-flash:generateContent \
-H 'Content-Type: application/json' -H 'Authorization: Be\***\*06' \
-d '{'contents': [{'role': 'user', 'parts': [{'text': 'Interview Transcript:\nи она имютабельная. Как еще можно делать строки? Приставим мы пишем Go и мы хотим обсуждать как можно строки у нас делать языки. Хорошо, вопрос как можно делать строки.'}]}], 'system_instruction': {'parts': [{'text': 'You are an invisible teleprompter for an interviewee.\nGiven the transcription of the interview question, provide a two-part response.\nFormat your output EXACTLY as follows:\n\n**TL;DR:** [One concise sentence summarizing the core answer]\n\n**Script:\*\* [A conversational, first-person response ("I would approach this by...", "The main difference is...") designed to be read aloud naturally.]\n'}]}, 'generationConfig': {'temperature': 0.3}}'

2026-06-09 00:06:35,720 - DEBUG -

POST Request Sent from LiteLLM:
curl -X POST \
https://aiplatform.googleapis.com/v1/projects/project-7d570aed-312f-4939-9a4/locations/global/publishers/google/models/gemini-2.5-flash:generateContent \
-H 'Content-Type: application/json' -H 'Authorization: Be\***\*06' \
-d '{'contents': [{'role': 'user', 'parts': [{'text': 'Interview Transcript:\nи она имютабельная. Как еще можно делать строки? Приставим мы пишем Go и мы хотим обсуждать как можно строки у нас делать языки. Хорошо, вопрос как можно делать строки.'}]}], 'system_instruction': {'parts': [{'text': 'You are an invisible teleprompter for an interviewee.\nGiven the transcription of the interview question, provide a two-part response.\nFormat your output EXACTLY as follows:\n\n**TL;DR:** [One concise sentence summarizing the core answer]\n\n**Script:\*\* [A conversational, first-person response ("I would approach this by...", "The main difference is...") designed to be read aloud naturally.]\n'}]}, 'generationConfig': {'temperature': 0.3}}'

2026-06-09 00:06:35,722 - DEBUG - connect_tcp.started host='aiplatform.googleapis.com' port=443 local_address=None timeout=600.0 socket_options=None
2026-06-09 00:06:36,078 - DEBUG - connect_tcp.complete return_value=<httpcore.\_backends.sync.SyncStream object at 0x123c73e10>
2026-06-09 00:06:36,079 - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x10fdcd950> server_hostname='aiplatform.googleapis.com' timeout=600.0
2026-06-09 00:06:36,463 - DEBUG - start_tls.complete return_value=<httpcore.\_backends.sync.SyncStream object at 0x126814950>
2026-06-09 00:06:36,464 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2026-06-09 00:06:36,464 - DEBUG - send_request_headers.complete
2026-06-09 00:06:36,464 - DEBUG - send_request_body.started request=<Request [b'POST']>
2026-06-09 00:06:36,464 - DEBUG - send_request_body.complete
2026-06-09 00:06:36,464 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2026-06-09 00:06:44,138 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Content-Type', b'application/json; charset=UTF-8'), (b'Vary', b'Origin'), (b'Vary', b'X-Origin'), (b'Vary', b'Referer'), (b'Content-Encoding', b'gzip'), (b'Date', b'Mon, 08 Jun 2026 21:06:44 GMT'), (b'Server', b'scaffolding on HTTPServer2'), (b'X-XSS-Protection', b'0'), (b'X-Frame-Options', b'SAMEORIGIN'), (b'X-Content-Type-Options', b'nosniff'), (b'Alt-Svc', b'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000'), (b'Transfer-Encoding', b'chunked')])
2026-06-09 00:06:44,141 - DEBUG - receive_response_body.started request=<Request [b'POST']>
2026-06-09 00:06:44,142 - DEBUG - receive_response_body.complete
2026-06-09 00:06:44,142 - DEBUG - response_closed.started
2026-06-09 00:06:44,142 - DEBUG - response_closed.complete
00:06:44 - LiteLLM:DEBUG: litellm_logging.py:1243 - RAW RESPONSE:
{
"candidates": [
{
"content": {
"role": "model",
"parts": [
{
"text": "**TL;DR:** In Go, strings are immutable and primarily created using literals, type conversions, or efficiently built with `strings.Builder` to manage dynamic construction.\n\n**Script:**\n\"In Go, strings are indeed immutable, as you mentioned, which is a fundamental aspect of how they work. The most common way to create them is through string literals, like `var s string = \"hello world\"`. We also have raw string literals using backticks, which are great for multi-line strings or when you want to avoid escaping special characters.\n\nBeyond literals, you can create strings by converting byte slices or rune slices directly into strings. For example, `string([]byte{'H', 'i'})` would create \"Hi\". You can also use `fmt.Sprintf` for formatted string creation.\n\nWhen it comes to operations that seem to modify strings, like concatenation using the `+` operator, it's important to remember that these actually create _new_ strings due to their immutability. This can be inefficient in loops.\n\nFor more dynamic or performance-critical string construction, especially when you're building a string piece by piece, the idiomatic approach in Go is to use `strings.Builder`. It provides an efficient way to append parts without constant reallocations, and then you can call its `String()` method to get the final immutable string.\""
}
]
},
"finishReason": "STOP",
"avgLogprobs": -0.581606979911209
}
],
"usageMetadata": {
"promptTokenCount": 135,
"candidatesTokenCount": 282,
"totalTokenCount": 1308,
"trafficType": "ON_DEMAND",
"promptTokensDetails": [
{
"modality": "TEXT",
"tokenCount": 135
}
],
"candidatesTokensDetails": [
{
"modality": "TEXT",
"tokenCount": 282
}
],
"thoughtsTokenCount": 891
},
"modelVersion": "gemini-2.5-flash",
"createTime": "2026-06-08T21:06:36.761061Z",
"responseId": "3C4nauW5LpSGz_IP8dLQyQM"
}

2026-06-09 00:06:44,143 - DEBUG - RAW RESPONSE:
{
"candidates": [
{
"content": {
"role": "model",
"parts": [
{
"text": "**TL;DR:** In Go, strings are immutable and primarily created using literals, type conversions, or efficiently built with `strings.Builder` to manage dynamic construction.\n\n**Script:**\n\"In Go, strings are indeed immutable, as you mentioned, which is a fundamental aspect of how they work. The most common way to create them is through string literals, like `var s string = \"hello world\"`. We also have raw string literals using backticks, which are great for multi-line strings or when you want to avoid escaping special characters.\n\nBeyond literals, you can create strings by converting byte slices or rune slices directly into strings. For example, `string([]byte{'H', 'i'})` would create \"Hi\". You can also use `fmt.Sprintf` for formatted string creation.\n\nWhen it comes to operations that seem to modify strings, like concatenation using the `+` operator, it's important to remember that these actually create _new_ strings due to their immutability. This can be inefficient in loops.\n\nFor more dynamic or performance-critical string construction, especially when you're building a string piece by piece, the idiomatic approach in Go is to use `strings.Builder`. It provides an efficient way to append parts without constant reallocations, and then you can call its `String()` method to get the final immutable string.\""
}
]
},
"finishReason": "STOP",
"avgLogprobs": -0.581606979911209
}
],
"usageMetadata": {
"promptTokenCount": 135,
"candidatesTokenCount": 282,
"totalTokenCount": 1308,
"trafficType": "ON_DEMAND",
"promptTokensDetails": [
{
"modality": "TEXT",
"tokenCount": 135
}
],
"candidatesTokensDetails": [
{
"modality": "TEXT",
"tokenCount": 282
}
],
"thoughtsTokenCount": 891
},
"modelVersion": "gemini-2.5-flash",
"createTime": "2026-06-08T21:06:36.761061Z",
"responseId": "3C4nauW5LpSGz_IP8dLQyQM"
}

00:06:44 - LiteLLM:INFO: utils.py:1656 - Wrapper: Completed Call, calling success_handler
2026-06-09 00:06:44,150 - INFO - Wrapper: Completed Call, calling success_handler
00:06:44 - LiteLLM:DEBUG: litellm_logging.py:2106 - Logging Details LiteLLM-Success Call: Cache_hit=None
2026-06-09 00:06:44,151 - DEBUG - Logging Details LiteLLM-Success Call: Cache_hit=None
00:06:44 - LiteLLM:DEBUG: cost_calculator.py:1262 - selected model name for cost calculation: vertex_ai/gemini-2.5-flash
2026-06-09 00:06:44,152 - DEBUG - selected model name for cost calculation: vertex_ai/gemini-2.5-flash
00:06:44 - LiteLLM:DEBUG: utils.py:5745 - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
2026-06-09 00:06:44,152 - DEBUG - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
00:06:44 - LiteLLM:DEBUG: utils.py:5745 - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
2026-06-09 00:06:44,153 - DEBUG - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
00:06:44 - LiteLLM:DEBUG: litellm_logging.py:1573 - response_cost: 0.0029730000000000004
2026-06-09 00:06:44,153 - DEBUG - response_cost: 0.0029730000000000004
00:06:44 - LiteLLM:DEBUG: utils.py:5745 - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
2026-06-09 00:06:44,154 - DEBUG - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
00:06:44 - LiteLLM:DEBUG: cost_calculator.py:1262 - selected model name for cost calculation: vertex_ai/gemini-2.5-flash
00:06:44 - LiteLLM:DEBUG: utils.py:5745 - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
2026-06-09 00:06:44,155 - DEBUG - selected model name for cost calculation: vertex_ai/gemini-2.5-flash
2026-06-09 00:06:44,155 - DEBUG - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
00:06:44 - LiteLLM:DEBUG: litellm_logging.py:1573 - response_cost: 0.0029730000000000004
2026-06-09 00:06:44,155 - DEBUG - response_cost: 0.0029730000000000004
2026-06-09 00:06:44,156 - INFO - Received LLM response.
