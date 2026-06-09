2026-06-09 01:31:02,258 - INFO - Starting Interview Assistant App (Dual Stream Whisper mode)
2026-06-09 01:31:02,588 - INFO - Loading Whisper model (small)... This may take a few seconds.
2026-06-09 01:31:02,677 - DEBUG - connect_tcp.started host='huggingface.co' port=443 local_address=None timeout=None socket_options=None
2026-06-09 01:31:02,833 - DEBUG - connect_tcp.complete return_value=<httpcore.\_backends.sync.SyncStream object at 0x122dc9310>
2026-06-09 01:31:02,833 - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x115b63d90> server_hostname='huggingface.co' timeout=None
2026-06-09 01:31:03,032 - DEBUG - start_tls.complete return_value=<httpcore.\_backends.sync.SyncStream object at 0x12269df30>
2026-06-09 01:31:03,032 - DEBUG - send_request_headers.started request=<Request [b'GET']>
2026-06-09 01:31:03,032 - DEBUG - send_request_headers.complete
2026-06-09 01:31:03,033 - DEBUG - send_request_body.started request=<Request [b'GET']>
2026-06-09 01:31:03,033 - DEBUG - send_request_body.complete
2026-06-09 01:31:03,033 - DEBUG - receive_response_headers.started request=<Request [b'GET']>
2026-06-09 01:31:03,444 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Content-Type', b'application/json; charset=utf-8'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'Date', b'Mon, 08 Jun 2026 22:31:03 GMT'), (b'content-encoding', b'gzip'), (b'ETag', b'W/"a27-vndQfbspAL31/eKATEOf36LyR8k"'), (b'X-Powered-By', b'huggingface-moon'), (b'X-Request-Id', b'Root=1-6a2742a7-56f28d890e8337da364087e0;14aa616a-4b62-4607-9370-e0146e8fb1c7'), (b'RateLimit', b'"api";r=499;t=293'), (b'RateLimit-Policy', b'"fixed window";"api";q=500;w=300'), (b'cross-origin-opener-policy', b'same-origin'), (b'Referrer-Policy', b'strict-origin-when-cross-origin'), (b'Access-Control-Max-Age', b'86400'), (b'Access-Control-Allow-Origin', b'https://huggingface.co'), (b'Vary', b'Origin'), (b'vary', b'Accept-Encoding'), (b'Access-Control-Expose-Headers', b'X-Repo-Commit,X-Request-Id,X-Error-Code,X-Error-Message,X-Total-Count,ETag,Link,Accept-Ranges,Content-Range,X-Linked-Size,X-Linked-ETag,X-Xet-Hash'), (b'X-Cache', b'Miss from cloudfront'), (b'Via', b'1.1 b80e8f7c73f4e5fd0596e4c456bfc524.cloudfront.net (CloudFront)'), (b'X-Amz-Cf-Pop', b'FRA56-P15'), (b'X-Amz-Cf-Id', b'Omza-RI2Hk2XovSAtmpttUHx45JKa2zuurdY9d2OuTzRO-9pqM7FRg==')])
2026-06-09 01:31:03,447 - DEBUG - receive_response_body.started request=<Request [b'GET']>
2026-06-09 01:31:03,449 - DEBUG - receive_response_body.complete
2026-06-09 01:31:03,449 - DEBUG - response_closed.started
2026-06-09 01:31:03,449 - DEBUG - response_closed.complete
2026-06-09 01:31:04,404 - INFO - Whisper model loaded!
2026-06-09 01:31:04,404 - DEBUG - Controller initialized
2026-06-09 01:31:04,405 - INFO - Default Mic found: JBL WAVE BUDS (Index 1)
2026-06-09 01:31:04,405 - INFO - System Audio (BlackHole) found: BlackHole 2ch (Index 3)
2026-06-09 01:31:04,463 - INFO - Microphone stream started.
2026-06-09 01:31:04,501 - INFO - System Audio (BlackHole) stream started.
2026-06-09 01:31:04,502 - INFO - Pynput listener started. Global hotkeys B, N, M active.
2026-06-09 01:31:25,610 - ERROR - Error in keyboard callback: 'NoneType' object has no attribute 'lower'
2026-06-09 01:31:38,959 - INFO - Triggered: START_CONTEXT
2026-06-09 01:32:06,291 - INFO - Triggered: TRIGGER_ANSWER
2026-06-09 01:32:06,296 - INFO - Retrieving last 60 seconds of audio...
2026-06-09 01:32:06,297 - INFO - Running Whisper transcription and diarization...
2026-06-09 01:32:06,297 - INFO - Processing audio with duration 00:27.328
2026-06-09 01:32:06,468 - INFO - VAD filter removed 00:24.368 of audio
2026-06-09 01:32:06,468 - DEBUG - VAD filter kept the following audio segments: [00:24.368 -> 00:27.328]
2026-06-09 01:32:07,132 - INFO - Detected language 'ru' with probability 0.96
2026-06-09 01:32:07,137 - DEBUG - Processing segment at 00:00.000
2026-06-09 01:32:07,965 - INFO - Processing audio with duration 00:27.328
2026-06-09 01:32:08,032 - INFO - VAD filter removed 00:00.432 of audio
2026-06-09 01:32:08,032 - DEBUG - VAD filter kept the following audio segments: [00:00.432 -> 00:27.328]
2026-06-09 01:32:08,576 - INFO - Detected language 'ru' with probability 0.89
2026-06-09 01:32:08,577 - DEBUG - Processing segment at 00:00.000
2026-06-09 01:32:11,104 - INFO - Diarized Transcript:
[Interviewer]: Это, конечно, печально, паника будет, это типичная штука, вот, чтение.
[Interviewer]: Да-да-да, все используешь. Куку, конечно, не слышал, нет? Что такое?
[Interviewer]: Нет.
[Interviewer]: Там, типа, две хэштабрицы, но, окей, хорошо.
[Interviewer]: Смотри, давай еще, что-то я поспрашиваю, вставка и чтение из неинцелизированной мапы.
[Candidate]: ставкой чтения и с ней цилисированный мок.
[Interviewer]: Вставка и чтение.
01:32:11 - LiteLLM:DEBUG: utils.py:485 -

2026-06-09 01:32:11,104 - DEBUG -

01:32:11 - LiteLLM:DEBUG: utils.py:485 - Request to litellm:
2026-06-09 01:32:11,105 - DEBUG - Request to litellm:
01:32:11 - LiteLLM:DEBUG: utils.py:485 - litellm.completion(model='vertex_ai/gemini-2.5-flash', messages=[{'role': 'system', 'content': 'You are an invisible teleprompter for an interviewee (referred to as [Candidate]).\nAnalyze the transcription of the technical interview conversation containing [Interviewer] and [Candidate] speaker tags.\nIdentify the last unanswered technical question asked by [Interviewer]. Ignore questions that [Candidate] has already answered correctly, unless the interviewer asked a follow-up.\nProvide a two-part response. Format your output EXACTLY as follows:\n\n**TL;DR:** [One concise sentence summarizing the core answer to the last active question]\n\n**Script:** [A conversational, first-person response ("I would approach this by...", "The main difference is...") designed to be read aloud naturally by the Candidate.]\n'}, {'role': 'user', 'content': 'Interview Transcript:\n[Interviewer]: Это, конечно, печально, паника будет, это типичная штука, вот, чтение.\n[Interviewer]: Да-да-да, все используешь. Куку, конечно, не слышал, нет? Что такое?\n[Interviewer]: Нет.\n[Interviewer]: Там, типа, две хэштабрицы, но, окей, хорошо.\n[Interviewer]: Смотри, давай еще, что-то я поспрашиваю, вставка и чтение из неинцелизированной мапы.\n[Candidate]: ставкой чтения и с ней цилисированный мок.\n[Interviewer]: Вставка и чтение.'}], temperature=0.3, stream=True)
2026-06-09 01:32:11,105 - DEBUG - litellm.completion(model='vertex_ai/gemini-2.5-flash', messages=[{'role': 'system', 'content': 'You are an invisible teleprompter for an interviewee (referred to as [Candidate]).\nAnalyze the transcription of the technical interview conversation containing [Interviewer] and [Candidate] speaker tags.\nIdentify the last unanswered technical question asked by [Interviewer]. Ignore questions that [Candidate] has already answered correctly, unless the interviewer asked a follow-up.\nProvide a two-part response. Format your output EXACTLY as follows:\n\n**TL;DR:** [One concise sentence summarizing the core answer to the last active question]\n\n**Script:** [A conversational, first-person response ("I would approach this by...", "The main difference is...") designed to be read aloud naturally by the Candidate.]\n'}, {'role': 'user', 'content': 'Interview Transcript:\n[Interviewer]: Это, конечно, печально, паника будет, это типичная штука, вот, чтение.\n[Interviewer]: Да-да-да, все используешь. Куку, конечно, не слышал, нет? Что такое?\n[Interviewer]: Нет.\n[Interviewer]: Там, типа, две хэштабрицы, но, окей, хорошо.\n[Interviewer]: Смотри, давай еще, что-то я поспрашиваю, вставка и чтение из неинцелизированной мапы.\n[Candidate]: ставкой чтения и с ней цилисированный мок.\n[Interviewer]: Вставка и чтение.'}], temperature=0.3, stream=True)
01:32:11 - LiteLLM:DEBUG: utils.py:485 -

2026-06-09 01:32:11,105 - DEBUG -

01:32:11 - LiteLLM:DEBUG: litellm_logging.py:563 - self.optional_params: {}
2026-06-09 01:32:11,113 - DEBUG - self.optional_params: {}
01:32:11 - LiteLLM:DEBUG: utils.py:485 - SYNC kwargs[caching]: False; litellm.cache: None; kwargs.get('cache')['no-cache']: False
2026-06-09 01:32:11,113 - DEBUG - SYNC kwargs[caching]: False; litellm.cache: None; kwargs.get('cache')['no-cache']: False
01:32:11 - LiteLLM:DEBUG: utils.py:5745 - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
2026-06-09 01:32:11,127 - DEBUG - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
01:32:11 - LiteLLM:DEBUG: utils.py:5745 - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
2026-06-09 01:32:11,133 - DEBUG - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
01:32:11 - LiteLLM:INFO: utils.py:4083 -
LiteLLM completion() model= gemini-2.5-flash; provider = vertex_ai
2026-06-09 01:32:11,134 - INFO -
LiteLLM completion() model= gemini-2.5-flash; provider = vertex_ai
01:32:11 - LiteLLM:DEBUG: utils.py:4086 -
LiteLLM: Params passed to completion() {'model': 'gemini-2.5-flash', 'functions': None, 'function_call': None, 'temperature': 0.3, 'top_p': None, 'n': None, 'stream': True, 'stream_options': None, 'stop': None, 'max_tokens': None, 'max_completion_tokens': None, 'modalities': None, 'prediction': None, 'audio': None, 'presence_penalty': None, 'frequency_penalty': None, 'logit_bias': None, 'user': None, 'custom_llm_provider': 'vertex_ai', 'response_format': None, 'seed': None, 'tools': None, 'tool_choice': None, 'max_retries': None, 'logprobs': None, 'top_logprobs': None, 'extra_headers': None, 'api_version': None, 'parallel_tool_calls': None, 'drop_params': None, 'allowed_openai_params': None, 'reasoning_effort': None, 'verbosity': None, 'additional_drop_params': None, 'messages': [{'role': 'system', 'content': 'You are an invisible teleprompter for an interviewee (referred to as [Candidate]).\nAnalyze the transcription of the technical interview conversation containing [Interviewer] and [Candidate] speaker tags.\nIdentify the last unanswered technical question asked by [Interviewer]. Ignore questions that [Candidate] has already answered correctly, unless the interviewer asked a follow-up.\nProvide a two-part response. Format your output EXACTLY as follows:\n\n**TL;DR:** [One concise sentence summarizing the core answer to the last active question]\n\n**Script:** [A conversational, first-person response ("I would approach this by...", "The main difference is...") designed to be read aloud naturally by the Candidate.]\n'}, {'role': 'user', 'content': 'Interview Transcript:\n[Interviewer]: Это, конечно, печально, паника будет, это типичная штука, вот, чтение.\n[Interviewer]: Да-да-да, все используешь. Куку, конечно, не слышал, нет? Что такое?\n[Interviewer]: Нет.\n[Interviewer]: Там, типа, две хэштабрицы, но, окей, хорошо.\n[Interviewer]: Смотри, давай еще, что-то я поспрашиваю, вставка и чтение из неинцелизированной мапы.\n[Candidate]: ставкой чтения и с ней цилисированный мок.\n[Interviewer]: Вставка и чтение.'}], 'thinking': None, 'web_search_options': None, 'safety_identifier': None, 'service_tier': None}
2026-06-09 01:32:11,134 - DEBUG -
LiteLLM: Params passed to completion() {'model': 'gemini-2.5-flash', 'functions': None, 'function_call': None, 'temperature': 0.3, 'top_p': None, 'n': None, 'stream': True, 'stream_options': None, 'stop': None, 'max_tokens': None, 'max_completion_tokens': None, 'modalities': None, 'prediction': None, 'audio': None, 'presence_penalty': None, 'frequency_penalty': None, 'logit_bias': None, 'user': None, 'custom_llm_provider': 'vertex_ai', 'response_format': None, 'seed': None, 'tools': None, 'tool_choice': None, 'max_retries': None, 'logprobs': None, 'top_logprobs': None, 'extra_headers': None, 'api_version': None, 'parallel_tool_calls': None, 'drop_params': None, 'allowed_openai_params': None, 'reasoning_effort': None, 'verbosity': None, 'additional_drop_params': None, 'messages': [{'role': 'system', 'content': 'You are an invisible teleprompter for an interviewee (referred to as [Candidate]).\nAnalyze the transcription of the technical interview conversation containing [Interviewer] and [Candidate] speaker tags.\nIdentify the last unanswered technical question asked by [Interviewer]. Ignore questions that [Candidate] has already answered correctly, unless the interviewer asked a follow-up.\nProvide a two-part response. Format your output EXACTLY as follows:\n\n**TL;DR:** [One concise sentence summarizing the core answer to the last active question]\n\n**Script:** [A conversational, first-person response ("I would approach this by...", "The main difference is...") designed to be read aloud naturally by the Candidate.]\n'}, {'role': 'user', 'content': 'Interview Transcript:\n[Interviewer]: Это, конечно, печально, паника будет, это типичная штука, вот, чтение.\n[Interviewer]: Да-да-да, все используешь. Куку, конечно, не слышал, нет? Что такое?\n[Interviewer]: Нет.\n[Interviewer]: Там, типа, две хэштабрицы, но, окей, хорошо.\n[Interviewer]: Смотри, давай еще, что-то я поспрашиваю, вставка и чтение из неинцелизированной мапы.\n[Candidate]: ставкой чтения и с ней цилисированный мок.\n[Interviewer]: Вставка и чтение.'}], 'thinking': None, 'web_search_options': None, 'safety_identifier': None, 'service_tier': None}
01:32:11 - LiteLLM:DEBUG: utils.py:4089 -
LiteLLM: Non-Default params passed to completion() {'temperature': 0.3, 'stream': True}
2026-06-09 01:32:11,135 - DEBUG -
LiteLLM: Non-Default params passed to completion() {'temperature': 0.3, 'stream': True}
01:32:11 - LiteLLM:DEBUG: utils.py:485 - Final returned optional params: {'temperature': 0.3, 'stream': True}
2026-06-09 01:32:11,135 - DEBUG - Final returned optional params: {'temperature': 0.3, 'stream': True}
01:32:11 - LiteLLM:DEBUG: litellm_logging.py:563 - self.optional_params: {'temperature': 0.3, 'stream': True}
2026-06-09 01:32:11,135 - DEBUG - self.optional_params: {'temperature': 0.3, 'stream': True}
01:32:11 - LiteLLM:DEBUG: utils.py:5745 - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
2026-06-09 01:32:11,135 - DEBUG - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
01:32:11 - LiteLLM:DEBUG: vertex_llm_base.py:913 - Checking cached credentials for project_id: project-7d570aed-312f-4939-9a4
2026-06-09 01:32:11,135 - DEBUG - Checking cached credentials for project_id: project-7d570aed-312f-4939-9a4
01:32:11 - LiteLLM:DEBUG: vertex_llm_base.py:938 - Credential cache key not found for project_id: project-7d570aed-312f-4939-9a4, loading new credentials
2026-06-09 01:32:11,135 - DEBUG - Credential cache key not found for project_id: project-7d570aed-312f-4939-9a4, loading new credentials
2026-06-09 01:32:11,141 - DEBUG - Checking '' for explicit credentials as part of auth process...
2026-06-09 01:32:11,141 - DEBUG - Checking Cloud SDK credentials as part of auth process...
2026-06-09 01:32:11,842 - DEBUG - Starting new HTTPS connection (1): oauth2.googleapis.com:443
2026-06-09 01:32:12,238 - DEBUG - https://oauth2.googleapis.com:443 "POST /token HTTP/1.1" 200 None
01:32:12 - LiteLLM:DEBUG: vertex_llm_base.py:965 - Validating credentials
2026-06-09 01:32:12,240 - DEBUG - Validating credentials
01:32:12 - LiteLLM:DEBUG: utils.py:5745 - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
2026-06-09 01:32:12,247 - DEBUG - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
01:32:12 - LiteLLM:DEBUG: litellm_logging.py:1170 -

POST Request Sent from LiteLLM:
curl -X POST \
https://aiplatform.googleapis.com/v1/projects/project-7d570aed-312f-4939-9a4/locations/global/publishers/google/models/gemini-2.5-flash:streamGenerateContent?alt=sse \
-H 'Content-Type: application/json' -H 'Authorization: Be\***\*06' \
-d '{'contents': [{'role': 'user', 'parts': [{'text': 'Interview Transcript:\n[Interviewer]: Это, конечно, печально, паника будет, это типичная штука, вот, чтение.\n[Interviewer]: Да-да-да, все используешь. Куку, конечно, не слышал, нет? Что такое?\n[Interviewer]: Нет.\n[Interviewer]: Там, типа, две хэштабрицы, но, окей, хорошо.\n[Interviewer]: Смотри, давай еще, что-то я поспрашиваю, вставка и чтение из неинцелизированной мапы.\n[Candidate]: ставкой чтения и с ней цилисированный мок.\n[Interviewer]: Вставка и чтение.'}]}], 'system_instruction': {'parts': [{'text': 'You are an invisible teleprompter for an interviewee (referred to as [Candidate]).\nAnalyze the transcription of the technical interview conversation containing [Interviewer] and [Candidate] speaker tags.\nIdentify the last unanswered technical question asked by [Interviewer]. Ignore questions that [Candidate] has already answered correctly, unless the interviewer asked a follow-up.\nProvide a two-part response. Format your output EXACTLY as follows:\n\n**TL;DR:** [One concise sentence summarizing the core answer to the last active question]\n\n**Script:\*\* [A conversational, first-person response ("I would approach this by...", "The main difference is...") designed to be read aloud naturally by the Candidate.]\n'}]}, 'generationConfig': {'temperature': 0.3}}'

2026-06-09 01:32:12,248 - DEBUG -

POST Request Sent from LiteLLM:
curl -X POST \
https://aiplatform.googleapis.com/v1/projects/project-7d570aed-312f-4939-9a4/locations/global/publishers/google/models/gemini-2.5-flash:streamGenerateContent?alt=sse \
-H 'Content-Type: application/json' -H 'Authorization: Be\***\*06' \
-d '{'contents': [{'role': 'user', 'parts': [{'text': 'Interview Transcript:\n[Interviewer]: Это, конечно, печально, паника будет, это типичная штука, вот, чтение.\n[Interviewer]: Да-да-да, все используешь. Куку, конечно, не слышал, нет? Что такое?\n[Interviewer]: Нет.\n[Interviewer]: Там, типа, две хэштабрицы, но, окей, хорошо.\n[Interviewer]: Смотри, давай еще, что-то я поспрашиваю, вставка и чтение из неинцелизированной мапы.\n[Candidate]: ставкой чтения и с ней цилисированный мок.\n[Interviewer]: Вставка и чтение.'}]}], 'system_instruction': {'parts': [{'text': 'You are an invisible teleprompter for an interviewee (referred to as [Candidate]).\nAnalyze the transcription of the technical interview conversation containing [Interviewer] and [Candidate] speaker tags.\nIdentify the last unanswered technical question asked by [Interviewer]. Ignore questions that [Candidate] has already answered correctly, unless the interviewer asked a follow-up.\nProvide a two-part response. Format your output EXACTLY as follows:\n\n**TL;DR:** [One concise sentence summarizing the core answer to the last active question]\n\n**Script:\*\* [A conversational, first-person response ("I would approach this by...", "The main difference is...") designed to be read aloud naturally by the Candidate.]\n'}]}, 'generationConfig': {'temperature': 0.3}}'

01:32:12 - LiteLLM:DEBUG: cost_calculator.py:1262 - selected model name for cost calculation: vertex_ai/gemini-2.5-flash
2026-06-09 01:32:12,253 - DEBUG - selected model name for cost calculation: vertex_ai/gemini-2.5-flash
01:32:12 - LiteLLM:DEBUG: token_counter.py:399 - messages in token_counter: None, text in token_counter:
2026-06-09 01:32:12,254 - DEBUG - messages in token_counter: None, text in token_counter:
01:32:12 - LiteLLM:DEBUG: utils.py:5745 - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
2026-06-09 01:32:12,256 - DEBUG - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
01:32:12 - LiteLLM:DEBUG: utils.py:5745 - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
2026-06-09 01:32:12,256 - DEBUG - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
01:32:12 - LiteLLM:DEBUG: litellm_logging.py:1573 - response_cost: 0.0
2026-06-09 01:32:12,257 - DEBUG - response_cost: 0.0
2026-06-09 01:32:12,259 - DEBUG - connect_tcp.started host='aiplatform.googleapis.com' port=443 local_address=None timeout=6000.0 socket_options=None
2026-06-09 01:32:12,438 - DEBUG - connect_tcp.complete return_value=<httpcore.\_backends.sync.SyncStream object at 0x1263e0e90>
2026-06-09 01:32:12,439 - DEBUG - start_tls.started ssl_context=<ssl.SSLContext object at 0x10f685bd0> server_hostname='aiplatform.googleapis.com' timeout=6000.0
2026-06-09 01:32:12,541 - DEBUG - start_tls.complete return_value=<httpcore.\_backends.sync.SyncStream object at 0x126524b90>
2026-06-09 01:32:12,541 - DEBUG - send_request_headers.started request=<Request [b'POST']>
2026-06-09 01:32:12,541 - DEBUG - send_request_headers.complete
2026-06-09 01:32:12,542 - DEBUG - send_request_body.started request=<Request [b'POST']>
2026-06-09 01:32:12,542 - DEBUG - send_request_body.complete
2026-06-09 01:32:12,542 - DEBUG - receive_response_headers.started request=<Request [b'POST']>
2026-06-09 01:32:17,418 - DEBUG - receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Content-Type', b'text/event-stream'), (b'Content-Disposition', b'attachment'), (b'Vary', b'Origin'), (b'Vary', b'X-Origin'), (b'Vary', b'Referer'), (b'Transfer-Encoding', b'chunked'), (b'Date', b'Mon, 08 Jun 2026 22:32:17 GMT'), (b'Server', b'scaffolding on HTTPServer2'), (b'X-XSS-Protection', b'0'), (b'X-Frame-Options', b'SAMEORIGIN'), (b'X-Content-Type-Options', b'nosniff'), (b'Alt-Svc', b'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000')])
01:32:17 - LiteLLM:DEBUG: litellm_logging.py:1243 - RAW RESPONSE:
first stream response received

2026-06-09 01:32:17,419 - DEBUG - RAW RESPONSE:
first stream response received

2026-06-09 01:32:17,420 - DEBUG - receive_response_body.started request=<Request [b'POST']>
01:32:17 - LiteLLM:DEBUG: vertex_and_google_ai_studio_gemini.py:3415 - RAW GEMINI CHUNK: {'candidates': [{'content': {'role': 'model', 'parts': [{'text': '**TL;'}]}}], 'usageMetadata': {'trafficType': 'ON_DEMAND'}, 'modelVersion': 'gemini-2.5-flash', 'createTime': '2026-06-08T22:32:12.854184Z', 'responseId': '7EInaqiRNMLemLAPwPGruA8'}
2026-06-09 01:32:17,420 - DEBUG - RAW GEMINI CHUNK: {'candidates': [{'content': {'role': 'model', 'parts': [{'text': '**TL;'}]}}], 'usageMetadata': {'trafficType': 'ON_DEMAND'}, 'modelVersion': 'gemini-2.5-flash', 'createTime': '2026-06-08T22:32:12.854184Z', 'responseId': '7EInaqiRNMLemLAPwPGruA8'}
01:32:17 - LiteLLM:DEBUG: streaming_handler.py:1021 - model_response.choices[0].delta: Delta(provider_specific_fields=None, content='**TL;', role='assistant', function_call=None, tool_calls=None, audio=None)
2026-06-09 01:32:17,426 - DEBUG - model_response.choices[0].delta: Delta(provider_specific_fields=None, content='**TL;', role='assistant', function_call=None, tool_calls=None, audio=None)
2026-06-09 01:32:17,426 - DEBUG - Using selector: KqueueSelector
01:32:17 - LiteLLM:DEBUG: utils.py:485 - Logging Details LiteLLM-Async Success Call, cache_hit=False
2026-06-09 01:32:17,430 - DEBUG - Logging Details LiteLLM-Async Success Call, cache_hit=False
01:32:17 - LiteLLM:DEBUG: vertex_and_google_ai_studio_gemini.py:3415 - RAW GEMINI CHUNK: {'candidates': [{'content': {'role': 'model', 'parts': [{'text': 'DR:** Accessing an uninitialized map for insertion or reading will result in undefined behavior, most likely a program crash due to invalid memory access.\n\n**Script:** "If we\'re talking about an uninitialized map, meaning it\'s been declared but its constructor hasn\'t been called or memory hasn\'t'}]}}], 'usageMetadata': {'trafficType': 'ON_DEMAND'}, 'modelVersion': 'gemini-2.5-flash', 'createTime': '2026-06-08T22:32:12.854184Z', 'responseId': '7EInaqiRNMLemLAPwPGruA8'}
2026-06-09 01:32:17,430 - DEBUG - RAW GEMINI CHUNK: {'candidates': [{'content': {'role': 'model', 'parts': [{'text': 'DR:** Accessing an uninitialized map for insertion or reading will result in undefined behavior, most likely a program crash due to invalid memory access.\n\n**Script:** "If we\'re talking about an uninitialized map, meaning it\'s been declared but its constructor hasn\'t been called or memory hasn\'t'}]}}], 'usageMetadata': {'trafficType': 'ON_DEMAND'}, 'modelVersion': 'gemini-2.5-flash', 'createTime': '2026-06-08T22:32:12.854184Z', 'responseId': '7EInaqiRNMLemLAPwPGruA8'}
01:32:17 - LiteLLM:DEBUG: streaming_handler.py:1021 - model_response.choices[0].delta: Delta(provider_specific_fields=None, content='DR:** Accessing an uninitialized map for insertion or reading will result in undefined behavior, most likely a program crash due to invalid memory access.\n\n**Script:** "If we\'re talking about an uninitialized map, meaning it\'s been declared but its constructor hasn\'t been called or memory hasn\'t', role=None, function_call=None, tool_calls=None, audio=None)
2026-06-09 01:32:17,431 - DEBUG - model_response.choices[0].delta: Delta(provider_specific_fields=None, content='DR:** Accessing an uninitialized map for insertion or reading will result in undefined behavior, most likely a program crash due to invalid memory access.\n\n**Script:** "If we\'re talking about an uninitialized map, meaning it\'s been declared but its constructor hasn\'t been called or memory hasn\'t', role=None, function_call=None, tool_calls=None, audio=None)
2026-06-09 01:32:17,431 - DEBUG - Using selector: KqueueSelector
01:32:17 - LiteLLM:DEBUG: utils.py:485 - Logging Details LiteLLM-Async Success Call, cache_hit=False
2026-06-09 01:32:17,432 - DEBUG - Logging Details LiteLLM-Async Success Call, cache_hit=False
01:32:17 - LiteLLM:DEBUG: litellm_logging.py:2106 - Logging Details LiteLLM-Success Call: Cache_hit=False
2026-06-09 01:32:17,432 - DEBUG - Logging Details LiteLLM-Success Call: Cache_hit=False
01:32:17 - LiteLLM:DEBUG: litellm_logging.py:2106 - Logging Details LiteLLM-Success Call: Cache_hit=False
2026-06-09 01:32:17,433 - DEBUG - Logging Details LiteLLM-Success Call: Cache_hit=False
01:32:17 - LiteLLM:DEBUG: vertex_and_google_ai_studio_gemini.py:3415 - RAW GEMINI CHUNK: {'candidates': [{'content': {'role': 'model', 'parts': [{'text': ' been allocated for its internal structures, then attempting either insertion or reading would lead to undefined behavior. In practice, this would almost certainly result in a program crash, such as a segmentation fault or access violation, because the map would try to operate on invalid memory addresses or non-existent data structures."'}]}, 'finishReason': 'STOP'}], 'usageMetadata': {'promptTokenCount': 296, 'candidatesTokenCount': 126, 'totalTokenCount': 1152, 'trafficType': 'ON_DEMAND', 'promptTokensDetails': [{'modality': 'TEXT', 'tokenCount': 296}], 'candidatesTokensDetails': [{'modality': 'TEXT', 'tokenCount': 126}], 'thoughtsTokenCount': 730}, 'modelVersion': 'gemini-2.5-flash', 'createTime': '2026-06-08T22:32:12.854184Z', 'responseId': '7EInaqiRNMLemLAPwPGruA8'}
2026-06-09 01:32:17,606 - DEBUG - RAW GEMINI CHUNK: {'candidates': [{'content': {'role': 'model', 'parts': [{'text': ' been allocated for its internal structures, then attempting either insertion or reading would lead to undefined behavior. In practice, this would almost certainly result in a program crash, such as a segmentation fault or access violation, because the map would try to operate on invalid memory addresses or non-existent data structures."'}]}, 'finishReason': 'STOP'}], 'usageMetadata': {'promptTokenCount': 296, 'candidatesTokenCount': 126, 'totalTokenCount': 1152, 'trafficType': 'ON_DEMAND', 'promptTokensDetails': [{'modality': 'TEXT', 'tokenCount': 296}], 'candidatesTokensDetails': [{'modality': 'TEXT', 'tokenCount': 126}], 'thoughtsTokenCount': 730}, 'modelVersion': 'gemini-2.5-flash', 'createTime': '2026-06-08T22:32:12.854184Z', 'responseId': '7EInaqiRNMLemLAPwPGruA8'}
01:32:17 - LiteLLM:DEBUG: streaming_handler.py:1021 - model_response.choices[0].delta: Delta(provider_specific_fields=None, content=' been allocated for its internal structures, then attempting either insertion or reading would lead to undefined behavior. In practice, this would almost certainly result in a program crash, such as a segmentation fault or access violation, because the map would try to operate on invalid memory addresses or non-existent data structures."', role=None, function_call=None, tool_calls=None, audio=None)
2026-06-09 01:32:17,612 - DEBUG - model_response.choices[0].delta: Delta(provider_specific_fields=None, content=' been allocated for its internal structures, then attempting either insertion or reading would lead to undefined behavior. In practice, this would almost certainly result in a program crash, such as a segmentation fault or access violation, because the map would try to operate on invalid memory addresses or non-existent data structures."', role=None, function_call=None, tool_calls=None, audio=None)
2026-06-09 01:32:17,613 - DEBUG - Using selector: KqueueSelector
01:32:17 - LiteLLM:DEBUG: utils.py:485 - Logging Details LiteLLM-Async Success Call, cache_hit=False
2026-06-09 01:32:17,613 - DEBUG - Logging Details LiteLLM-Async Success Call, cache_hit=False
01:32:17 - LiteLLM:DEBUG: litellm_logging.py:2106 - Logging Details LiteLLM-Success Call: Cache_hit=False
2026-06-09 01:32:17,613 - DEBUG - Logging Details LiteLLM-Success Call: Cache_hit=False
2026-06-09 01:32:17,746 - DEBUG - receive_response_body.complete
2026-06-09 01:32:17,747 - DEBUG - response_closed.started
2026-06-09 01:32:17,747 - DEBUG - response_closed.complete
2026-06-09 01:32:17,750 - DEBUG - Using selector: KqueueSelector
01:32:17 - LiteLLM:DEBUG: utils.py:485 - Logging Details LiteLLM-Async Success Call, cache_hit=False
2026-06-09 01:32:17,750 - DEBUG - Logging Details LiteLLM-Async Success Call, cache_hit=False
01:32:17 - LiteLLM:DEBUG: litellm_logging.py:2106 - Logging Details LiteLLM-Success Call: Cache_hit=False
2026-06-09 01:32:17,752 - DEBUG - Logging Details LiteLLM-Success Call: Cache_hit=False
2026-06-09 01:32:17,756 - INFO - Received LLM response.
01:32:17 - LiteLLM:DEBUG: litellm_logging.py:2106 - Logging Details LiteLLM-Success Call: Cache_hit=False
2026-06-09 01:32:17,756 - DEBUG - Logging Details LiteLLM-Success Call: Cache_hit=False
01:32:17 - LiteLLM:DEBUG: litellm_logging.py:2137 - Logging Details LiteLLM-Success Call streaming complete
2026-06-09 01:32:17,756 - DEBUG - Logging Details LiteLLM-Success Call streaming complete
01:32:17 - LiteLLM:DEBUG: cost_calculator.py:1262 - selected model name for cost calculation: vertex_ai/gemini-2.5-flash
2026-06-09 01:32:17,757 - DEBUG - selected model name for cost calculation: vertex_ai/gemini-2.5-flash
01:32:17 - LiteLLM:DEBUG: litellm_logging.py:1573 - response_cost: 0.0022288000000000004
2026-06-09 01:32:17,758 - DEBUG - response_cost: 0.0022288000000000004
01:32:17 - LiteLLM:DEBUG: utils.py:5745 - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
2026-06-09 01:32:17,759 - DEBUG - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
01:32:17 - LiteLLM:DEBUG: utils.py:5745 - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
2026-06-09 01:32:17,759 - DEBUG - checking potential_model_names in litellm.model_cost: {'split_model': 'gemini-2.5-flash', 'combined_model_name': 'vertex_ai/gemini-2.5-flash', 'stripped_model_name': 'gemini-2.5-flash', 'combined_stripped_model_name': 'vertex_ai/gemini-2.5-flash', 'custom_llm_provider': 'vertex_ai'}
