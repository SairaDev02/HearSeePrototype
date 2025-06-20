================================================================================= test session starts =================================================================================
platform win32 -- Python 3.12.1, pytest-8.3.5, pluggy-1.5.0 -- C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\FerdinandM\Desktop\HearSeePrototype
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.8.0, cov-6.1.1
collected 139 items                                                                                                                                                                    

tests/functional/test_responsive_design.py::TestResponsiveDesign::test_chat_interface_responsive_layout PASSED                                                                   [  0%]
tests/functional/test_responsive_design.py::TestResponsiveDesign::test_gallery_responsive_configuration PASSED                                                                   [  1%]
tests/functional/test_responsive_design.py::TestResponsiveDesign::test_chatbot_responsive_configuration PASSED                                                                   [  2%]
tests/functional/test_responsive_design.py::TestResponsiveDesign::test_mobile_viewport_adaptation PASSED                                                                         [  2%]
tests/functional/test_responsive_design.py::TestResponsiveDesign::test_guide_interface_responsive_content PASSED                                                                 [  3%]
tests/functional/test_responsive_design.py::TestResponsiveDesign::test_cross_component_interactions PASSED                                                                       [  4%]
tests/functional/test_responsive_design.py::TestResponsiveDesign::test_ui_state_transitions PASSED                                                                               [  5%]
tests/integration/test_error_handling.py::TestErrorHandling::test_oversized_image_handling 
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------
2025-06-20 12:21:00 [    INFO] Starting text extraction from image (image_utils.py:48)
2025-06-20 12:21:00 [ WARNING] Image size validation failed: Image size (15.0MB) exceeds maximum allowed size (10MB) (image_utils.py:52)
PASSED                                                                                                                                                                           [  5%]
tests/integration/test_error_handling.py::TestErrorHandling::test_missing_api_token_handling 
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------
2025-06-20 12:21:00 [    INFO] Starting text extraction from image (image_utils.py:48)
2025-06-20 12:21:00 [   ERROR] Replicate API token not found in environment variables (replicate_service.py:99)
2025-06-20 12:21:00 [   ERROR] API not available: Error: Replicate API token not found. Set REPLICATE_API_TOKEN in your .env file. (replicate_service.py:128)
2025-06-20 12:21:00 [   ERROR] Error extracting text from image: Error: Replicate API token not found. Set REPLICATE_API_TOKEN in your .env file. (image_utils.py:85)
Traceback (most recent call last):
  File "C:\Users\FerdinandM\Desktop\HearSeePrototype\utils\image_utils.py", line 69, in extract_text
    result = ReplicateService.run_vision_model(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\Desktop\HearSeePrototype\services\replicate_service.py", line 129, in run_vision_model
    raise ValueError(error_msg)
ValueError: Error: Replicate API token not found. Set REPLICATE_API_TOKEN in your .env file.
PASSED                                                                                                                                                                           [  6%]
tests/integration/test_error_handling.py::TestErrorHandling::test_api_error_handling 
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------
2025-06-20 12:21:00 [    INFO] Starting text extraction from image (image_utils.py:48)
2025-06-20 12:21:00 [   ERROR] Error extracting text from image: API rate limit exceeded (image_utils.py:85)
Traceback (most recent call last):
  File "C:\Users\FerdinandM\Desktop\HearSeePrototype\utils\image_utils.py", line 69, in extract_text
    result = ReplicateService.run_vision_model(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\Lib\unittest\mock.py", line 1134, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\Lib\unittest\mock.py", line 1138, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\Lib\unittest\mock.py", line 1193, in _execute_mock_call
    raise effect
Exception: API rate limit exceeded
PASSED                                                                                                                                                                           [  7%] 
tests/integration/test_error_handling.py::TestErrorHandling::test_network_failure_handling_in_tts PASSED                                                                         [  7%] 
tests/integration/test_error_handling.py::TestErrorHandling::test_invalid_voice_type_handling
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [ WARNING] TTS validation failed: Invalid voice type 'Invalid Voice' (validators.py:188)
PASSED                                                                                                                                                                           [  8%] 
tests/integration/test_error_handling.py::TestErrorHandling::test_invalid_speed_handling
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [ WARNING] TTS validation failed: Speed 0.1 out of range (validators.py:200)
2025-06-20 12:21:00 [ WARNING] TTS validation failed: Speed 3.0 out of range (validators.py:200)
PASSED                                                                                                                                                                           [  9%] 
tests/integration/test_error_handling.py::TestErrorHandling::test_empty_text_handling_in_tts PASSED                                                                              [ 10%] 
tests/integration/test_error_handling.py::TestErrorHandling::test_missing_image_handling
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [ WARNING] Image validation failed: No image provided (validators.py:79)
PASSED                                                                                                                                                                           [ 10%] 
tests/integration/test_error_handling.py::TestErrorHandling::test_corrupted_image_handling
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [    INFO] Starting text extraction from image (image_utils.py:48)
2025-06-20 12:21:00 [ WARNING] Image size validation failed: Error checking image size: cannot write mode F as PNG (image_utils.py:52)
PASSED                                                                                                                                                                           [ 11%] 
tests/integration/test_error_handling.py::TestErrorHandling::test_server_error_handling
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [    INFO] Starting text extraction from image (image_utils.py:48)
2025-06-20 12:21:00 [   ERROR] Error extracting text from image: Server returned status code 500 (image_utils.py:85)
Traceback (most recent call last):
  File "C:\Users\FerdinandM\Desktop\HearSeePrototype\utils\image_utils.py", line 69, in extract_text
    result = ReplicateService.run_vision_model(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\Lib\unittest\mock.py", line 1134, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\Lib\unittest\mock.py", line 1138, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\Lib\unittest\mock.py", line 1193, in _execute_mock_call
    raise effect
Exception: Server returned status code 500
PASSED                                                                                                                                                                           [ 12%] 
tests/integration/test_error_handling.py::TestErrorHandling::test_timeout_handling
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [    INFO] Starting text extraction from image (image_utils.py:48)
2025-06-20 12:21:00 [   ERROR] Error extracting text from image: Request timed out after 30 seconds (image_utils.py:85)
Traceback (most recent call last):
  File "C:\Users\FerdinandM\Desktop\HearSeePrototype\utils\image_utils.py", line 69, in extract_text
    result = ReplicateService.run_vision_model(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\Lib\unittest\mock.py", line 1134, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\Lib\unittest\mock.py", line 1138, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\Lib\unittest\mock.py", line 1193, in _execute_mock_call
    raise effect
Exception: Request timed out after 30 seconds
PASSED                                                                                                                                                                           [ 12%] 
tests/integration/test_error_handling.py::TestErrorHandling::test_resource_constraint_handling
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [    INFO] Starting text extraction from image (image_utils.py:48)
2025-06-20 12:21:00 [   ERROR] Error extracting text from image: Out of memory (image_utils.py:85)
Traceback (most recent call last):
  File "C:\Users\FerdinandM\Desktop\HearSeePrototype\utils\image_utils.py", line 69, in extract_text
    result = ReplicateService.run_vision_model(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\Lib\unittest\mock.py", line 1134, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\Lib\unittest\mock.py", line 1138, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\Lib\unittest\mock.py", line 1193, in _execute_mock_call
    raise effect
MemoryError: Out of memory
PASSED                                                                                                                                                                           [ 13%] 
tests/integration/test_image_processing_pipeline.py::TestImageProcessingPipeline::test_extract_text_pipeline
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [    INFO] Starting text extraction from image (image_utils.py:48)
2025-06-20 12:21:00 [    INFO] Image included in vision model request (replicate_service.py:140)
2025-06-20 12:21:00 [    INFO] Vision model API call completed successfully (replicate_service.py:148)
2025-06-20 12:21:00 [    INFO] Text extraction completed in 0.00s with 7 words (image_utils.py:78)
PASSED                                                                                                                                                                           [ 14%] 
tests/integration/test_image_processing_pipeline.py::TestImageProcessingPipeline::test_caption_image_pipeline
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [    INFO] Starting image captioning (image_utils.py:121)
2025-06-20 12:21:00 [    INFO] Image included in vision model request (replicate_service.py:140)
2025-06-20 12:21:00 [    INFO] Vision model API call completed successfully (replicate_service.py:148)
2025-06-20 12:21:00 [    INFO] Image captioning completed in 0.00s with 8 words (image_utils.py:149)
PASSED                                                                                                                                                                           [ 15%] 
tests/integration/test_image_processing_pipeline.py::TestImageProcessingPipeline::test_summarize_image_pipeline
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [    INFO] Starting image summarization (image_utils.py:188)
2025-06-20 12:21:00 [    INFO] Image included in vision model request (replicate_service.py:140)
2025-06-20 12:21:00 [    INFO] Vision model API call completed successfully (replicate_service.py:148)
2025-06-20 12:21:00 [    INFO] Image summarization completed in 0.00s with 8 words (image_utils.py:213)
PASSED                                                                                                                                                                           [ 15%] 
tests/integration/test_image_processing_pipeline.py::TestImageProcessingPipeline::test_image_processing_with_api_unavailable
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [    INFO] Starting text extraction from image (image_utils.py:48)
2025-06-20 12:21:00 [   ERROR] Replicate API token not found in environment variables (replicate_service.py:99)
2025-06-20 12:21:00 [   ERROR] API not available: Error: Replicate API token not found. Set REPLICATE_API_TOKEN in your .env file. (replicate_service.py:128)
2025-06-20 12:21:00 [   ERROR] Error extracting text from image: Error: Replicate API token not found. Set REPLICATE_API_TOKEN in your .env file. (image_utils.py:85)
Traceback (most recent call last):
  File "C:\Users\FerdinandM\Desktop\HearSeePrototype\utils\image_utils.py", line 69, in extract_text
    result = ReplicateService.run_vision_model(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\Desktop\HearSeePrototype\services\replicate_service.py", line 129, in run_vision_model
    raise ValueError(error_msg)
ValueError: Error: Replicate API token not found. Set REPLICATE_API_TOKEN in your .env file.
PASSED                                                                                                                                                                           [ 16%] 
tests/integration/test_image_processing_pipeline.py::TestImageProcessingPipeline::test_end_to_end_image_processing
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [    INFO] Starting text extraction from image (image_utils.py:48)
2025-06-20 12:21:00 [    INFO] Text extraction completed in 0.00s with 2 words (image_utils.py:78)
PASSED                                                                                                                                                                           [ 17%] 
tests/integration/test_image_processing_pipeline.py::TestImageProcessingPipeline::test_image_size_validation_integration
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [    INFO] Starting text extraction from image (image_utils.py:48)
2025-06-20 12:21:00 [ WARNING] Image size validation failed: Image size (75.0MB) exceeds maximum allowed size (10MB) (image_utils.py:52)
PASSED                                                                                                                                                                           [ 17%] 
tests/integration/test_image_processing_pipeline.py::TestImageProcessingPipeline::test_image_processing_error_handling
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------
2025-06-20 12:21:00 [    INFO] Starting text extraction from image (image_utils.py:48)
2025-06-20 12:21:00 [   ERROR] Error extracting text from image: Test error (image_utils.py:85)
Traceback (most recent call last):
  File "C:\Users\FerdinandM\Desktop\HearSeePrototype\utils\image_utils.py", line 69, in extract_text
    result = ReplicateService.run_vision_model(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\Lib\unittest\mock.py", line 1134, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\Lib\unittest\mock.py", line 1138, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\Lib\unittest\mock.py", line 1193, in _execute_mock_call
    raise effect
Exception: Test error
PASSED                                                                                                                                                                           [ 18%] 
tests/integration/test_image_processing_pipeline.py::TestImageProcessingPipeline::test_image_conversion_pipeline
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [    INFO] Starting text extraction from image (image_utils.py:48)
2025-06-20 12:21:00 [    INFO] Text extraction completed in 0.00s with 2 words (image_utils.py:78)
PASSED                                                                                                                                                                           [ 19%] 
tests/integration/test_tts_pipeline.py::TestTTSPipeline::test_tts_pipeline_success
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [    INFO] Running TTS model with voice: af_river, speed: 1.0 (replicate_service.py:185)
2025-06-20 12:21:00 [    INFO] TTS model API call completed successfully (replicate_service.py:197)
PASSED                                                                                                                                                                           [ 20%] 
tests/integration/test_tts_pipeline.py::TestTTSPipeline::test_tts_pipeline_with_validation
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [    INFO] Running TTS model with voice: af_river, speed: 1.0 (replicate_service.py:185)
2025-06-20 12:21:00 [    INFO] TTS model API call completed successfully (replicate_service.py:197)
PASSED                                                                                                                                                                           [ 20%] 
tests/integration/test_tts_pipeline.py::TestTTSPipeline::test_tts_pipeline_with_chat_history
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [    INFO] Running TTS model with voice: af_river, speed: 1.0 (replicate_service.py:185)
2025-06-20 12:21:00 [    INFO] TTS model API call completed successfully (replicate_service.py:197)
PASSED                                                                                                                                                                           [ 21%] 
tests/integration/test_tts_pipeline.py::TestTTSPipeline::test_tts_pipeline_api_unavailable
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [   ERROR] Replicate API token not found in environment variables (replicate_service.py:99)
PASSED                                                                                                                                                                           [ 22%] 
tests/integration/test_tts_pipeline.py::TestTTSPipeline::test_tts_pipeline_empty_text PASSED                                                                                     [ 23%] 
tests/integration/test_tts_pipeline.py::TestTTSPipeline::test_tts_pipeline_api_error PASSED                                                                                      [ 23%] 
tests/integration/test_tts_pipeline.py::TestTTSPipeline::test_tts_pipeline_download_error
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [    INFO] Running TTS model with voice: af_river, speed: 1.0 (replicate_service.py:185)
2025-06-20 12:21:00 [    INFO] TTS model API call completed successfully (replicate_service.py:197)
PASSED                                                                                                                                                                           [ 24%] 
tests/integration/test_tts_pipeline.py::TestTTSPipeline::test_tts_pipeline_file_cleanup
------------------------------------------------------------------------------------ live log call ------------------------------------------------------------------------------------ 
2025-06-20 12:21:00 [    INFO] Running TTS model with voice: af_river, speed: 1.0 (replicate_service.py:185)
2025-06-20 12:21:00 [    INFO] TTS model API call completed successfully (replicate_service.py:197)
PASSED                                                                                                                                                                           [ 25%] 
tests/integration/test_tts_pipeline.py::TestTTSPipeline::test_end_to_end_tts_pipeline PASSED                                                                                     [ 25%] 
tests/integration/test_ui_interactions.py::TestUIInteractions::test_image_upload_enables_buttons PASSED                                                                          [ 26%]
tests/integration/test_ui_interactions.py::TestUIInteractions::test_chat_message_processing_flow PASSED                                                                          [ 27%] 
tests/integration/test_ui_interactions.py::TestUIInteractions::test_extract_text_user_journey PASSED                                                                             [ 28%] 
tests/integration/test_ui_interactions.py::TestUIInteractions::test_tts_user_journey PASSED                                                                                      [ 28%] 
tests/integration/test_ui_interactions.py::TestUIInteractions::test_end_to_end_chat_flow PASSED                                                                                  [ 29%] 
tests/unit/config/test_logging_config.py::TestLoggingConfig::test_log_constants PASSED                                                                                           [ 30%] 
tests/unit/config/test_logging_config.py::TestLoggingConfig::test_log_directory_creation PASSED                                                                                  [ 30%] 
tests/unit/config/test_logging_config.py::TestLoggingConfig::test_configure_logging PASSED                                                                                       [ 31%] 
tests/unit/config/test_logging_config.py::TestLoggingConfig::test_get_logger PASSED                                                                                              [ 32%] 
tests/unit/config/test_logging_config.py::TestLoggingConfig::test_console_handler_configuration PASSED                                                                           [ 33%] 
tests/unit/config/test_logging_config.py::TestLoggingConfig::test_file_handlers_configuration PASSED                                                                             [ 33%] 
tests/unit/config/test_logging_config.py::TestLoggingConfig::test_third_party_logging_levels PASSED                                                                              [ 34%] 
tests/unit/config/test_settings.py::TestSettings::test_model_constants PASSED                                                                                                    [ 35%] 
tests/unit/config/test_settings.py::TestSettings::test_api_configuration PASSED                                                                                                  [ 35%]
tests/unit/config/test_settings.py::TestSettings::test_image_settings PASSED                                                                                                     [ 36%] 
tests/unit/config/test_settings.py::TestSettings::test_init_history PASSED                                                                                                       [ 37%] 
tests/unit/config/test_settings.py::TestSettings::test_voice_types PASSED                                                                                                        [ 38%] 
tests/unit/config/test_settings.py::TestSettings::test_tts_speed_range PASSED                                                                                                    [ 38%] 
tests/unit/config/test_settings.py::TestSettings::test_default_tts_settings PASSED                                                                                               [ 39%] 
tests/unit/config/test_settings.py::TestSettings::test_settings_reload PASSED                                                                                                    [ 40%] 
tests/unit/services/test_image_service.py::TestImageService::test_image_to_base64_with_numpy_array PASSED                                                                        [ 41%] 
tests/unit/services/test_image_service.py::TestImageService::test_image_to_base64_with_pil_image PASSED                                                                          [ 41%] 
tests/unit/services/test_image_service.py::TestImageService::test_image_to_base64_with_none PASSED                                                                               [ 42%] 
tests/unit/services/test_image_service.py::TestImageService::test_image_to_base64_with_exception PASSED                                                                          [ 43%] 
tests/unit/services/test_image_service.py::TestImageService::test_verify_image_size_success PASSED                                                                               [ 43%]
tests/unit/services/test_image_service.py::TestImageService::test_verify_image_size_none PASSED                                                                                  [ 44%] 
tests/unit/services/test_image_service.py::TestImageService::test_verify_image_size_too_large PASSED                                                                             [ 45%] 
tests/unit/services/test_image_service.py::TestImageService::test_preprocess_image PASSED                                                                                        [ 46%] 
tests/unit/services/test_image_service.py::TestImageService::test_preprocess_image_none PASSED                                                                                   [ 46%] 
tests/unit/services/test_image_service.py::TestImageService::test_extract_image_metadata PASSED                                                                                  [ 47%] 
tests/unit/services/test_image_service.py::TestImageService::test_extract_image_metadata_none PASSED                                                                             [ 48%] 
tests/unit/services/test_replicate_service.py::TestReplicateService::test_verify_api_available_success PASSED                                                                    [ 48%] 
tests/unit/services/test_replicate_service.py::TestReplicateService::test_verify_api_available_failure PASSED                                                                    [ 49%] 
tests/unit/services/test_replicate_service.py::TestReplicateService::test_run_vision_model PASSED                                                                                [ 50%]
tests/unit/services/test_replicate_service.py::TestReplicateService::test_run_vision_model_api_unavailable PASSED                                                                [ 51%] 
tests/unit/services/test_replicate_service.py::TestReplicateService::test_run_vision_model_exception PASSED                                                                      [ 51%] 
tests/unit/services/test_replicate_service.py::TestReplicateService::test_run_tts_model PASSED                                                                                   [ 52%] 
tests/unit/services/test_tts_service.py::TestTTSService::test_validate_voice_type_with_valid_voice PASSED                                                                        [ 53%] 
tests/unit/services/test_tts_service.py::TestTTSService::test_validate_voice_type_with_invalid_voice PASSED                                                                      [ 53%] 
tests/unit/services/test_tts_service.py::TestTTSService::test_validate_voice_type_with_none PASSED                                                                               [ 54%] 
tests/unit/services/test_tts_service.py::TestTTSService::test_validate_speed_with_valid_speed PASSED                                                                             [ 55%] 
tests/unit/services/test_tts_service.py::TestTTSService::test_validate_speed_below_minimum PASSED                                                                                [ 56%] 
tests/unit/services/test_tts_service.py::TestTTSService::test_validate_speed_above_maximum PASSED                                                                                [ 56%] 
tests/unit/services/test_tts_service.py::TestTTSService::test_validate_speed_with_none PASSED                                                                                    [ 57%] 
tests/unit/services/test_tts_service.py::TestTTSService::test_process_audio_success PASSED                                                                                       [ 58%]
tests/unit/services/test_tts_service.py::TestTTSService::test_process_audio_api_unavailable PASSED                                                                               [ 58%] 
tests/unit/services/test_tts_service.py::TestTTSService::test_process_audio_empty_text PASSED                                                                                    [ 59%] 
tests/unit/services/test_tts_service.py::TestTTSService::test_process_audio_request_error PASSED                                                                                 [ 60%] 
tests/unit/services/test_tts_service.py::TestTTSService::test_process_audio_exception PASSED                                                                                     [ 61%] 
tests/unit/services/test_tts_service.py::TestTTSService::test_cleanup_audio_file PASSED                                                                                          [ 61%] 
tests/unit/services/test_tts_service.py::TestTTSService::test_cleanup_audio_file_nonexistent PASSED                                                                              [ 62%] 
tests/unit/services/test_tts_service.py::TestTTSService::test_cleanup_audio_file_exception PASSED                                                                                [ 63%]
tests/unit/ui/test_chat_interface.py::TestChatInterface::test_create_interface_module_function PASSED                                                                            [ 64%] 
tests/unit/ui/test_chat_interface.py::TestChatInterface::test_create_interface_components PASSED                                                                                 [ 64%] 
tests/unit/ui/test_chat_interface.py::TestChatInterface::test_interface_structure PASSED                                                                                         [ 65%]
tests/unit/ui/test_chat_interface.py::TestChatInterface::test_button_initial_states PASSED                                                                                       [ 66%] 
tests/unit/ui/test_chat_interface.py::TestChatInterface::test_responsive_layout PASSED                                                                                           [ 66%] 
tests/unit/ui/test_components.py::TestUIComponents::test_chatbot_component_creation PASSED                                                                                       [ 67%] 
tests/unit/ui/test_components.py::TestUIComponents::test_image_instruction_creation PASSED                                                                                       [ 68%] 
tests/unit/ui/test_components.py::TestUIComponents::test_voice_type_dropdown_creation PASSED                                                                                     [ 69%] 
tests/unit/ui/test_components.py::TestUIComponents::test_speed_slider_creation PASSED                                                                                            [ 69%] 
tests/unit/ui/test_components.py::TestUIComponents::test_mllm_status_creation PASSED                                                                                             [ 70%] 
tests/unit/ui/test_components.py::TestUIComponents::test_component_edge_cases PASSED                                                                                             [ 71%] 
tests/unit/ui/test_guide_interface.py::TestGuideInterface::test_create_guide_interface_module_function PASSED                                                                    [ 71%] 
tests/unit/ui/test_guide_interface.py::TestGuideInterface::test_create_guide_content PASSED                                                                                      [ 72%] 
tests/unit/ui/test_guide_interface.py::TestGuideInterface::test_guide_sections_completeness PASSED                                                                               [ 73%] 
tests/unit/ui/test_guide_interface.py::TestGuideInterface::test_guide_creation_with_actual_component PASSED                                                                      [ 74%] 
tests/unit/ui/test_guide_interface.py::TestGuideInterface::test_guide_contains_all_features PASSED                                                                               [ 74%] 
tests/unit/ui/test_guide_interface.py::TestGuideInterface::test_guide_contains_troubleshooting_info PASSED                                                                       [ 75%] 
tests/unit/utils/test_image_utils.py::TestImageUtils::test_extract_text_success PASSED                                                                                           [ 76%] 
tests/unit/utils/test_image_utils.py::TestImageUtils::test_extract_text_invalid_size PASSED                                                                                      [ 76%] 
tests/unit/utils/test_image_utils.py::TestImageUtils::test_extract_text_base64_failure PASSED                                                                                    [ 77%] 
tests/unit/utils/test_image_utils.py::TestImageUtils::test_extract_text_api_exception PASSED                                                                                     [ 78%] 
tests/unit/utils/test_image_utils.py::TestImageUtils::test_caption_image_success PASSED                                                                                          [ 79%] 
tests/unit/utils/test_image_utils.py::TestImageUtils::test_caption_image_invalid_size PASSED                                                                                     [ 79%] 
tests/unit/utils/test_image_utils.py::TestImageUtils::test_caption_image_base64_failure PASSED                                                                                   [ 80%] 
tests/unit/utils/test_image_utils.py::TestImageUtils::test_caption_image_api_exception PASSED                                                                                    [ 81%] 
tests/unit/utils/test_image_utils.py::TestImageUtils::test_summarize_image_success PASSED                                                                                        [ 82%]
tests/unit/utils/test_image_utils.py::TestImageUtils::test_summarize_image_invalid_size PASSED                                                                                   [ 82%] 
tests/unit/utils/test_image_utils.py::TestImageUtils::test_summarize_image_base64_failure PASSED                                                                                 [ 83%] 
tests/unit/utils/test_image_utils.py::TestImageUtils::test_summarize_image_api_exception PASSED                                                                                  [ 84%] 
tests/unit/utils/test_image_utils.py::TestImageUtils::test_with_existing_history PASSED                                                                                          [ 84%] 
tests/unit/utils/test_logger.py::TestLogger::test_configure_logging PASSED                                                                                                       [ 85%] 
tests/unit/utils/test_logger.py::TestLogger::test_get_logger PASSED                                                                                                              [ 86%]
tests/unit/utils/test_logger.py::TestLogger::test_log_directory_creation PASSED                                                                                                  [ 87%] 
tests/unit/utils/test_logger.py::TestLogger::test_log_format PASSED                                                                                                              [ 87%] 
tests/unit/utils/test_logger.py::TestLogger::test_third_party_logging_levels PASSED                                                                                              [ 88%] 
tests/unit/utils/test_logger.py::TestLogger::test_logging_functionality PASSED                                                                                                   [ 89%] 
tests/unit/utils/test_validators.py::TestValidators::test_validate_message_valid PASSED                                                                                          [ 89%] 
tests/unit/utils/test_validators.py::TestValidators::test_validate_message_empty PASSED                                                                                          [ 90%] 
tests/unit/utils/test_validators.py::TestValidators::test_validate_message_whitespace PASSED                                                                                     [ 91%] 
tests/unit/utils/test_validators.py::TestValidators::test_validate_image_input_valid PASSED                                                                                      [ 92%] 
tests/unit/utils/test_validators.py::TestValidators::test_validate_image_input_none PASSED                                                                                       [ 92%]
tests/unit/utils/test_validators.py::TestValidators::test_validate_history_valid PASSED                                                                                          [ 93%] 
tests/unit/utils/test_validators.py::TestValidators::test_validate_history_none PASSED                                                                                           [ 94%] 
tests/unit/utils/test_validators.py::TestValidators::test_validate_history_invalid_type PASSED                                                                                   [ 94%] 
tests/unit/utils/test_validators.py::TestValidators::test_get_last_bot_message_valid PASSED                                                                                      [ 95%] 
tests/unit/utils/test_validators.py::TestValidators::test_get_last_bot_message_empty PASSED                                                                                      [ 96%] 
tests/unit/utils/test_validators.py::TestValidators::test_validate_tts_input_valid PASSED                                                                                        [ 97%] 
tests/unit/utils/test_validators.py::TestValidators::test_validate_tts_input_empty_text PASSED                                                                                   [ 97%] 
tests/unit/utils/test_validators.py::TestValidators::test_validate_tts_input_invalid_speed_value PASSED                                                                          [ 98%] 
tests/unit/utils/test_validators.py::TestValidators::test_validate_tts_input_speed_too_low PASSED                                                                                [ 99%] 
tests/unit/utils/test_validators.py::TestValidators::test_validate_tts_input_speed_too_high PASSED                                                                               [100%] 

================================================================================== warnings summary =================================================================================== 
..\..\AppData\Local\Programs\Python\Python312\Lib\site-packages\websockets\legacy\__init__.py:6
  C:\Users\FerdinandM\AppData\Local\Programs\Python\Python312\Lib\site-packages\websockets\legacy\__init__.py:6: DeprecationWarning: websockets.legacy is deprecated; see https://websockets.readthedocs.io/en/stable/howto/upgrade.html for upgrade instructions
    warnings.warn(  # deprecated in 14.0 - 2024-11-09

tests/functional/test_responsive_design.py: 5 warnings
tests/integration/test_ui_interactions.py: 2 warnings
tests/unit/ui/test_chat_interface.py: 4 warnings
tests/unit/ui/test_components.py: 1 warning
  C:\Users\FerdinandM\Desktop\HearSeePrototype\ui\components.py:41: UserWarning: You have not specified a value for the `type` parameter. Defaulting to the 'tuples' format for chatbot messages, but this is deprecated and will be removed in a future version of Gradio. Please set type='messages' instead, which uses openai-style dictionaries with 'role' and 'content' keys.
    return gr.Chatbot(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=================================================================================== tests coverage ==================================================================================== 
___________________________________________________________________ coverage: platform win32, python 3.12.1-final-0 ___________________________________________________________________ 

Name                                                  Stmts   Miss  Cover
-------------------------------------------------------------------------
app.py                                                  129    110    15%
config\__init__.py                                        2      0   100%
config\logging_config.py                                 36      1    97%
config\settings.py                                        9      0   100%
services\__init__.py                                      7      0   100%
services\image_service.py                                56      3    95%
services\replicate_service.py                            55      5    91%
services\tts_service.py                                  57      6    89%
tests\__init__.py                                         0      0   100%
tests\conftest.py                                        53     14    74%
tests\fixtures\__init__.py                                0      0   100%
tests\fixtures\test_data.py                              37     12    68%
tests\functional\__init__.py                              0      0   100%
tests\functional\test_responsive_design.py               64      0   100%
tests\integration\__init__.py                             0      0   100%
tests\integration\test_error_handling.py                 82      0   100%
tests\integration\test_image_processing_pipeline.py      62      0   100%
tests\integration\test_tts_pipeline.py                  101      0   100%
tests\integration\test_ui_interactions.py                79      0   100%
tests\test_config.py                                     13      0   100%
tests\unit\__init__.py                                    0      0   100%
tests\unit\config\__init__.py                             0      0   100%
tests\unit\config\test_settings.py                       58      2    97%
tests\unit\services\__init__.py                           0      0   100%
tests\unit\services\test_image_service.py                65      2    97%
tests\unit\services\test_replicate_service.py            35      0   100%
tests\unit\services\test_tts_service.py                  86      0   100%
tests\unit\ui\__init__.py                                 0      0   100%
tests\unit\ui\test_chat_interface.py                     60      1    98%
tests\unit\ui\test_components.py                         78      0   100%
tests\unit\ui\test_guide_interface.py                    54      0   100%
tests\unit\utils\__init__.py                              0      0   100%
tests\unit\utils\test_image_utils.py                     87      0   100%
tests\unit\utils\test_validators.py                      61      0   100%
ui\__init__.py                                           35     20    43%
ui\chat_interface.py                                     34      0   100%
ui\components.py                                         12      0   100%
ui\guide_interface.py                                     7      0   100%
utils\__init__.py                                        43     35    19%
utils\image_utils.py                                     97      1    99%
utils\logger.py                                          63     45    29%
utils\validators.py                                      62      0   100%
-------------------------------------------------------------------------
TOTAL                                                  1779    257    86%
Coverage HTML written to dir htmlcov
========================================================================== 139 passed, 13 warnings in 7.40s ===========================================================================