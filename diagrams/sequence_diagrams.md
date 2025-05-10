# HearSee Application - Sequence Diagrams

This document contains sequence diagrams for the HearSee application, showing the interactions between actors and system components for each use case defined in the use case diagram.

## Table of Contents

1. [Upload Image](#1-upload-image)
2. [Send Message](#2-send-message)
3. [Regenerate Response](#3-regenerate-response)
4. [Clear Chat History](#4-clear-chat-history)
5. [Extract Text from Image](#5-extract-text-from-image)
6. [Caption Image](#6-caption-image)
7. [Summarize Image](#7-summarize-image)
8. [Convert Text to Speech](#8-convert-text-to-speech)
9. [Select Voice Type](#9-select-voice-type)
10. [Adjust Speech Speed](#10-adjust-speech-speed)
11. [Process Image with Vision Model](#11-process-image-with-vision-model)
12. [Generate Audio with TTS Model](#12-generate-audio-with-tts-model)

## 1. Upload Image

This sequence diagram shows the interactions when a user uploads an image to the application.

```plantuml
@startuml Upload Image Sequence
actor User
participant "UI (ChatInterface)" as UI
participant "app.py" as App
participant "ImageService" as ImgSvc
participant "utils.validators" as Val

User -> UI: Click "Upload Image" button
activate UI
UI -> App: upload_btn.upload()
activate App

App -> App: lambda x: (x, [x] if x is not None else [])
note right
  This lambda function:
  1. Stores image in hidden component
  2. Creates a list with the image for gallery display
end note

App -> Val: validate_image_input(image)
activate Val
Val --> App: valid, error_message
deactivate Val

alt Image invalid
    App --> UI: Return error message
else Image valid
    App -> ImgSvc: verify_image_size(image)
    activate ImgSvc
    ImgSvc --> App: size_valid, size_msg
    deactivate ImgSvc
    
    alt Image size invalid
        App --> UI: Return error message
    else Image size valid
        App -> App: update_button_state(image)
        App --> UI: Return updated UI state
    end
end

deactivate App
UI --> User: Display image in gallery
UI --> User: Enable image-related buttons
UI --> User: Hide image instruction message
deactivate UI

note right of App
  The update_button_state function:
  1. Enables the Send, Extract, Caption, and Summarize buttons
  2. Sets image_uploaded_state to true
  3. Hides the image instruction message
end note

@enduml
```

## 2. Send Message

This sequence diagram shows the interactions when a user sends a message related to an uploaded image.

```plantuml
@startuml Send Message Sequence
actor User
participant "UI (ChatInterface)" as UI
participant "app.py" as App
participant "utils.validators" as Val
participant "ImageService" as ImgSvc
participant "ReplicateService" as RepSvc
participant "Replicate API" as API

User -> UI: Enter message and click "Send"
activate UI
UI -> App: send_btn.click()
activate App

App -> App: start_processing()
App --> UI: Update UI to show processing state
App -> App: locked_chat_response(message, history, metrics, image)
activate App #DarkSalmon
App -> App: process_chat_message(message, history, metrics, image)
activate App #LightBlue

' Validate message
App -> Val: validate_message(message)
activate Val
Val --> App: valid, error_message
deactivate Val

alt Message invalid
    App --> App: Return error in history
else Message valid
    ' Validate image size
    App -> ImgSvc: verify_image_size(image)
    activate ImgSvc
    ImgSvc --> App: size_valid, size_msg
    deactivate ImgSvc
    
    alt Image size invalid
        App --> App: Return error in history
    else Image size valid
        ' Check API availability
        App -> RepSvc: verify_api_available()
        activate RepSvc
        RepSvc --> App: api_available, error_msg
        deactivate RepSvc
        
        alt API unavailable
            App --> App: Return error in history
        else API available
            ' Validate image requirement
            App -> Val: validate_image_input(image)
            activate Val
            Val --> App: valid, error_message
            deactivate Val
            
            alt Image invalid
                App --> App: Return error in history
            else Image valid
                ' Process the message
                App -> ImgSvc: image_to_base64(image)
                activate ImgSvc
                ImgSvc --> App: img_str (base64 encoded image)
                deactivate ImgSvc
                
                App -> App: Build system_prompt and context
                App -> RepSvc: run_vision_model(prompt, img_str)
                activate RepSvc
                
                note right
                  This is an asynchronous operation
                  that may take several seconds
                end note
                
                RepSvc -> API: replicate.run(QWEN_VL_MODEL, input=api_params)
                activate API
                
                ' Potential timeout or network error
                alt Network error or timeout
                    API --> RepSvc: Raise exception
                    RepSvc --> App: Raise RuntimeError
                    App --> App: Return error in history
                else Successful API call
                    API --> RepSvc: output (model response)
                    deactivate API
                    RepSvc --> App: result (processed response)
                    deactivate RepSvc
                    
                    App -> App: Calculate performance metrics
                    App --> App: Return updated history and metrics
                end
            end
        end
    end
end

deactivate App #LightBlue
App --> App: updated_history, updated_metrics, ""
deactivate App #DarkSalmon

App -> App: end_processing(chatbot, metrics, image_uploaded_state)
App --> UI: Update UI with response and restore interactive state
deactivate App

UI --> User: Display bot response in chat
UI --> User: Display performance metrics
UI --> User: Restore interactive state
deactivate UI

@enduml
```

## 3. Regenerate Response

This sequence diagram shows the interactions when a user requests to regenerate the last response.

```plantuml
@startuml Regenerate Response Sequence
actor User
participant "UI (ChatInterface)" as UI
participant "app.py" as App
participant "ImageService" as ImgSvc
participant "ReplicateService" as RepSvc
participant "Replicate API" as API

User -> UI: Click "Regenerate" button
activate UI
UI -> App: regenerate_btn.click()
activate App

App -> App: start_processing()
App --> UI: Update UI to show processing state
App -> App: regenerate_last_response(history, metrics, image)
activate App #DarkSalmon

alt History is empty
    App --> App: Return unchanged history and metrics
else History has entries
    App -> App: Extract last_user_msg from history[-1][0]
    App -> App: Remove last conversation pair (new_history = history[:-1])
    
    App -> App: process_chat_message(last_user_msg, new_history, metrics, image)
    activate App #LightBlue
    
    note right of App
      This follows the same flow as the Send Message sequence,
      but uses the last user message instead of a new one
    end note
    
    App -> ImgSvc: verify_image_size(image)
    App -> RepSvc: verify_api_available()
    App -> ImgSvc: image_to_base64(image)
    App -> RepSvc: run_vision_model(prompt, img_str)
    RepSvc -> API: replicate.run(QWEN_VL_MODEL, input=api_params)
    API --> RepSvc: output (model response)
    RepSvc --> App: result (processed response)
    
    App -> App: Calculate performance metrics
    App --> App: Return updated history and metrics
    deactivate App #LightBlue
end

App --> App: response, updated_metrics
deactivate App #DarkSalmon

App -> App: end_processing(chatbot, metrics, image_uploaded_state)
App --> UI: Update UI with regenerated response and restore interactive state
deactivate App

UI --> User: Display regenerated bot response in chat
UI --> User: Display updated performance metrics
UI --> User: Restore interactive state
deactivate UI

@enduml
```

## 4. Clear Chat History

This sequence diagram shows the interactions when a user clears the chat history.

```plantuml
@startuml Clear Chat History Sequence
actor User
participant "UI (ChatInterface)" as UI
participant "app.py" as App
participant "config.settings" as Config

User -> UI: Click "Clear History" button
activate UI
UI -> App: clear_btn.click()
activate App

App -> App: clear_interface_state()
activate App #DarkSalmon

App -> Config: INIT_HISTORY
activate Config
Config --> App: Initial empty history
deactivate Config

App --> App: Return reset UI state values
deactivate App #DarkSalmon

App --> UI: Update UI components with reset values
deactivate App

UI --> User: Display empty chat history
UI --> User: Reset gallery (remove images)
UI --> User: Disable image-dependent buttons
UI --> User: Show image instruction message
deactivate UI

@enduml
```

## 5. Extract Text from Image

This sequence diagram shows the interactions when a user requests to extract text from an uploaded image.

```plantuml
@startuml Extract Text from Image Sequence
actor User
participant "UI (ChatInterface)" as UI
participant "app.py" as App
participant "ImageUtils" as ImgUtils
participant "ImageService" as ImgSvc
participant "ReplicateService" as RepSvc
participant "Replicate API" as API

User -> UI: Click "Extract Text" button
activate UI
UI -> App: extract_btn.click()
activate App

App -> App: start_processing()
App --> UI: Update UI to show processing state
App -> ImgUtils: extract_text(image, chatbot)
activate ImgUtils

ImgUtils -> ImgSvc: verify_image_size(image)
activate ImgSvc
ImgSvc --> ImgUtils: size_valid, size_msg
deactivate ImgSvc

alt Image size invalid
    ImgUtils --> App: Return error in history and metrics
else Image size valid
    ImgUtils -> ImgSvc: image_to_base64(image)
    activate ImgSvc
    ImgSvc --> ImgUtils: img_str (base64 encoded image)
    deactivate ImgSvc
    
    ImgUtils -> ImgUtils: Craft specialized OCR prompts
    ImgUtils -> RepSvc: run_vision_model(prompt, img_str)
    activate RepSvc
    RepSvc -> API: replicate.run(QWEN_VL_MODEL, input=api_params)
    activate API
    API --> RepSvc: output (extracted text)
    deactivate API
    RepSvc --> ImgUtils: result (processed text)
    deactivate RepSvc
    
    ImgUtils -> ImgUtils: Calculate performance metrics
    ImgUtils --> App: Return updated history with extracted text and metrics
end

deactivate ImgUtils

App -> App: end_processing(chatbot, metrics, image_uploaded_state)
App --> UI: Update UI with extracted text and restore interactive state
deactivate App

UI --> User: Display extracted text in chat
UI --> User: Display performance metrics
UI --> User: Restore interactive state
deactivate UI

@enduml
```

## 6. Caption Image

This sequence diagram shows the interactions when a user requests to generate a caption for an uploaded image.

```plantuml
@startuml Caption Image Sequence
actor User
participant "UI (ChatInterface)" as UI
participant "app.py" as App
participant "ImageUtils" as ImgUtils
participant "ImageService" as ImgSvc
participant "ReplicateService" as RepSvc
participant "Replicate API" as API

User -> UI: Click "Caption Image" button
activate UI
UI -> App: caption_btn.click()
activate App

App -> App: start_processing()
App --> UI: Update UI to show processing state
App -> ImgUtils: caption_image(image, chatbot)
activate ImgUtils

ImgUtils -> ImgSvc: verify_image_size(image)
activate ImgSvc
ImgSvc --> ImgUtils: size_valid, size_msg
deactivate ImgSvc

alt Image size invalid
    ImgUtils --> App: Return error in history and metrics
else Image size valid
    ImgUtils -> ImgSvc: image_to_base64(image)
    activate ImgSvc
    ImgSvc --> ImgUtils: img_str (base64 encoded image)
    deactivate ImgSvc
    
    ImgUtils -> ImgUtils: Craft specialized caption prompts
    ImgUtils -> RepSvc: run_vision_model(prompt, img_str)
    activate RepSvc
    RepSvc -> API: replicate.run(QWEN_VL_MODEL, input=api_params)
    activate API
    API --> RepSvc: output (image caption)
    deactivate API
    RepSvc --> ImgUtils: result (processed caption)
    deactivate RepSvc
    
    ImgUtils -> ImgUtils: Calculate performance metrics
    ImgUtils --> App: Return updated history with caption and metrics
end

deactivate ImgUtils

App -> App: end_processing(chatbot, metrics, image_uploaded_state)
App --> UI: Update UI with image caption and restore interactive state
deactivate App

UI --> User: Display image caption in chat
UI --> User: Display performance metrics
UI --> User: Restore interactive state
deactivate UI

@enduml
```

## 7. Summarize Image

This sequence diagram shows the interactions when a user requests to generate a detailed summary of an uploaded image.

```plantuml
@startuml Summarize Image Sequence
actor User
participant "UI (ChatInterface)" as UI
participant "app.py" as App
participant "ImageUtils" as ImgUtils
participant "ImageService" as ImgSvc
participant "ReplicateService" as RepSvc
participant "Replicate API" as API

User -> UI: Click "Summarize Image" button
activate UI
UI -> App: summarize_btn.click()
activate App

App -> App: start_processing()
App --> UI: Update UI to show processing state
App -> ImgUtils: summarize_image(image, chatbot)
activate ImgUtils

ImgUtils -> ImgSvc: verify_image_size(image)
activate ImgSvc
ImgSvc --> ImgUtils: size_valid, size_msg
deactivate ImgSvc

alt Image size invalid
    ImgUtils --> App: Return error in history and metrics
else Image size valid
    ImgUtils -> ImgSvc: image_to_base64(image)
    activate ImgSvc
    ImgSvc --> ImgUtils: img_str (base64 encoded image)
    deactivate ImgSvc
    
    ImgUtils -> ImgUtils: Craft comprehensive analysis prompt
    ImgUtils -> RepSvc: run_vision_model(prompt, img_str)
    activate RepSvc
    RepSvc -> API: replicate.run(QWEN_VL_MODEL, input=api_params)
    activate API
    API --> RepSvc: output (detailed summary)
    deactivate API
    RepSvc --> ImgUtils: result (processed summary)
    deactivate RepSvc
    
    ImgUtils -> ImgUtils: Calculate performance metrics
    ImgUtils --> App: Return updated history with summary and metrics
end

deactivate ImgUtils

App -> App: end_processing(chatbot, metrics, image_uploaded_state)
App --> UI: Update UI with image summary and restore interactive state
deactivate App

UI --> User: Display image summary in chat
UI --> User: Display performance metrics
UI --> User: Restore interactive state
deactivate UI

@enduml
```

## 8. Convert Text to Speech

This sequence diagram shows the interactions when a user converts the last bot response to speech.

```plantuml
@startuml Convert Text to Speech Sequence
actor User
participant "UI (ChatInterface)" as UI
participant "app.py" as App
participant "Validators" as Val
participant "TTSService" as TTS
participant "ReplicateService" as RepSvc
participant "Replicate API" as API
participant "File System" as FS

User -> UI: Click "Play Last Response" button
activate UI
UI -> App: tts_btn.click()
activate App

App -> App: start_processing()
App --> UI: Update UI to show processing state
App -> App: text_to_speech_conversion(history, voice_type, speed)
activate App #DarkSalmon

App -> Val: get_last_bot_message(history)
activate Val
Val --> App: text (last bot message)
deactivate Val

App -> Val: validate_tts_input(text, voice_type, speed)
activate Val
Val --> App: valid, error_message
deactivate Val

alt TTS input invalid
    App --> App: Return None, error_message
else TTS input valid
    App -> TTS: process_audio(text, voice_type, speed)
    activate TTS
    
    TTS -> RepSvc: verify_api_available()
    activate RepSvc
    RepSvc --> TTS: api_available, error_msg
    deactivate RepSvc
    
    alt API unavailable
        TTS --> App: None, error_msg
    else API available
        alt Text is empty
            TTS --> App: None, "No text to convert to speech."
        else Text is valid
            TTS -> TTS: validate_voice_type(voice_type)
            TTS -> TTS: validate_speed(speed)
            
            TTS -> RepSvc: run_tts_model(text, voice_id, safe_speed)
            activate RepSvc
            
            note right
              This is an asynchronous operation
              that may take several seconds
            end note
            
            RepSvc -> API: replicate.run(KOKORO_TTS_MODEL, input=params)
            activate API
            
            alt API call failed
                API --> RepSvc: Raise exception
                RepSvc --> TTS: Raise RuntimeError
                TTS --> App: None, error_message
            else API call succeeded
                API --> RepSvc: audio_url
                deactivate API
                RepSvc --> TTS: audio_url
                deactivate RepSvc
                
                TTS -> API: requests.get(audio_url)
                activate API
                
                alt Network error
                    API --> TTS: Raise exception
                    TTS --> App: None, error_message
                else Download succeeded
                    API --> TTS: response (audio content)
                    deactivate API
                    
                    alt response.status_code != 200
                        TTS --> App: None, error_message
                    else response.status_code == 200
                        TTS -> TTS: _create_temp_audio_file(response.content)
                        activate TTS #LightBlue
                        TTS -> FS: Write audio content to temporary file
                        activate FS
                        FS --> TTS: temp_file.name (file path)
                        deactivate FS
                        TTS --> TTS: Return temp_path
                        deactivate TTS #LightBlue
                        
                        TTS --> App: temp_path, status_message
                    end
                end
            end
        end
    end
    
    deactivate TTS
end

App --> App: audio_file, status_message
deactivate App #DarkSalmon

App -> App: end_processing_tts(audio_val, status_val, image_uploaded_state)
App --> UI: Update UI with audio player and restore interactive state
deactivate App

UI --> User: Display audio player with generated speech
UI --> User: Display TTS status message
UI --> User: Restore interactive state
deactivate UI

@enduml
```

## 9. Select Voice Type

This sequence diagram shows the interactions when a user selects a voice type for text-to-speech conversion.

```plantuml
@startuml Select Voice Type Sequence
actor User
participant "UI (ChatInterface)" as UI
participant "TTSService" as TTS
participant "config.settings" as Config

User -> UI: Select voice type from dropdown
activate UI

UI -> UI: Store selected voice_type value
note right
  The voice_type is stored in the UI component
  and will be used when the TTS button is clicked
end note

alt voice_type is None
    UI -> UI: Use default voice type
else voice_type is provided
    UI -> TTS: validate_voice_type(voice_type)
    activate TTS
    
    TTS -> Config: DEFAULT_VOICE
    activate Config
    Config --> TTS: default_voice
    deactivate Config
    
    TTS -> Config: VOICE_TYPES
    activate Config
    Config --> TTS: voice_types_mapping
    deactivate Config
    
    alt voice_type not in VOICE_TYPES
        TTS -> TTS: Use VOICE_TYPES[DEFAULT_VOICE]
    else voice_type in VOICE_TYPES
        TTS -> TTS: Use VOICE_TYPES[voice_type]
    end
    
    TTS --> UI: validated_voice_id
    deactivate TTS
end

UI --> User: Update UI to show selected voice type
deactivate UI

@enduml
```

## 10. Adjust Speech Speed

This sequence diagram shows the interactions when a user adjusts the speech speed for text-to-speech conversion.

```plantuml
@startuml Adjust Speech Speed Sequence
actor User
participant "UI (ChatInterface)" as UI
participant "TTSService" as TTS
participant "config.settings" as Config

User -> UI: Adjust speed slider
activate UI

UI -> UI: Store selected speed value
note right
  The speed is stored in the UI component
  and will be used when the TTS button is clicked
end note

alt speed is None
    UI -> UI: Use default speed
else speed is provided
    UI -> TTS: validate_speed(speed)
    activate TTS
    
    TTS -> Config: DEFAULT_SPEED
    activate Config
    Config --> TTS: default_speed
    deactivate Config
    
    TTS -> Config: TTS_SPEED_RANGE
    activate Config
    Config --> TTS: min_speed, max_speed
    deactivate Config
    
    TTS -> TTS: Clamp speed to range: max(min_speed, min(max_speed, float(speed)))
    TTS --> UI: safe_speed
    deactivate TTS
end

UI --> User: Update UI to show adjusted speed
deactivate UI

@enduml
```

## 11. Process Image with Vision Model

This sequence diagram shows the internal interactions when processing an image with the vision model.

```plantuml
@startuml Process Image with Vision Model Sequence
participant "Application" as App
participant "ReplicateService" as RepSvc
participant "Replicate API Provider" as API
participant "Environment" as Env

App -> RepSvc: run_vision_model(prompt, image_base64, max_tokens)
activate RepSvc

RepSvc -> RepSvc: verify_api_available()
activate RepSvc #LightBlue
RepSvc -> Env: os.environ["REPLICATE_API_TOKEN"]
activate Env
Env --> RepSvc: token or KeyError
deactivate Env

alt Token not found
    RepSvc --> RepSvc: Return False, error_msg
    RepSvc --> App: Raise ValueError(error_msg)
else Token found
    RepSvc --> RepSvc: Return True, ""
end
deactivate RepSvc #LightBlue

alt API available
    RepSvc -> RepSvc: Prepare api_params with prompt and max_tokens
    
    alt image_base64 is provided
        RepSvc -> RepSvc: Add media parameter with base64 image
    end
    
    RepSvc -> API: replicate.run(QWEN_VL_MODEL, input=api_params)
    activate API
    
    note right of API
      The Qwen VL model processes the image and prompt,
      generating a text response based on visual understanding.
      This is an asynchronous operation that may take
      several seconds to complete.
    end note
    
    alt API call failed (network error, timeout, etc.)
        API --> RepSvc: Raise exception
        RepSvc -> RepSvc: Log error
        RepSvc --> App: Raise RuntimeError with details
    else API call succeeded
        API --> RepSvc: output (model response)
        deactivate API
        
        alt output is a list
            RepSvc -> RepSvc: Join output chunks ("".join(output))
        end
        
        RepSvc --> App: Return processed response
    end
end

deactivate RepSvc

@enduml
```

## 12. Generate Audio with TTS Model

This sequence diagram shows the internal interactions when generating audio with the TTS model.

```plantuml
@startuml Generate Audio with TTS Model Sequence
participant "Application" as App
participant "TTSService" as TTS
participant "ReplicateService" as RepSvc
participant "Replicate API Provider" as API
participant "File System" as FS
participant "Environment" as Env
participant "config.settings" as Config

App -> TTS: process_audio(text, voice_type, speed)
activate TTS

TTS -> RepSvc: verify_api_available()
activate RepSvc
RepSvc -> Env: os.environ["REPLICATE_API_TOKEN"]
activate Env
Env --> RepSvc: token or KeyError
deactivate Env
RepSvc --> TTS: api_available, error_msg
deactivate RepSvc

alt API unavailable
    TTS --> App: None, error_msg
else API available
    alt Text is empty
        TTS --> App: None, "No text to convert to speech."
    else Text is valid
        TTS -> TTS: validate_voice_type(voice_type)
        activate TTS #LightBlue
        
        TTS -> Config: DEFAULT_VOICE
        activate Config
        Config --> TTS: default_voice
        deactivate Config
        
        TTS -> Config: VOICE_TYPES
        activate Config
        Config --> TTS: voice_types_mapping
        deactivate Config
        
        alt voice_type is None
            TTS -> TTS: Use DEFAULT_VOICE
        else voice_type not in VOICE_TYPES
            TTS -> TTS: Use VOICE_TYPES[DEFAULT_VOICE]
        else voice_type in VOICE_TYPES
            TTS -> TTS: Use VOICE_TYPES[voice_type]
        end
        
        TTS --> TTS: Return voice_id
        deactivate TTS #LightBlue
        
        TTS -> TTS: validate_speed(speed)
        activate TTS #LightBlue
        
        TTS -> Config: DEFAULT_SPEED
        activate Config
        Config --> TTS: default_speed
        deactivate Config
        
        TTS -> Config: TTS_SPEED_RANGE
        activate Config
        Config --> TTS: min_speed, max_speed
        deactivate Config
        
        alt speed is None
            TTS -> TTS: Use DEFAULT_SPEED
        else
            TTS -> TTS: Clamp speed to range: max(min_speed, min(max_speed, float(speed)))
        end
        
        TTS --> TTS: Return safe_speed
        deactivate TTS #LightBlue
        
        TTS -> RepSvc: run_tts_model(text, voice_id, safe_speed)
        activate RepSvc
        
        RepSvc -> RepSvc: verify_api_available()
        
        alt API unavailable
            RepSvc --> TTS: Raise ValueError(error_msg)
        else API available
            RepSvc -> API: replicate.run(KOKORO_TTS_MODEL, input=params)
            activate API
            
            note right of API
              The Kokoro TTS model converts the text to speech
              using the specified voice and speed parameters.
              This is an asynchronous operation that may take
              several seconds to complete.
            end note
            
            API --> RepSvc: audio_url
            deactivate API
            
            RepSvc --> TTS: audio_url
        end
        
        deactivate RepSvc
        
        TTS -> API: requests.get(audio_url)
        activate API
        API --> TTS: response (audio content)
        deactivate API
        
        alt response.status_code == 200
            TTS -> TTS: _create_temp_audio_file(response.content)
            activate TTS #DarkSalmon
            
            TTS -> FS: Create NamedTemporaryFile(suffix=".wav", delete=False)
            activate FS
            FS --> TTS: temp_file
            TTS -> FS: temp_file.write(content)
            TTS -> FS: temp_file.name
            FS --> TTS: file path
            deactivate FS
            
            TTS --> TTS: Return temp_path
            deactivate TTS #DarkSalmon
            
            TTS --> App: temp_path, status_message
        else
            TTS --> App: None, error_message
        end
    end
end

deactivate TTS

@enduml
```

## Conclusion

These sequence diagrams illustrate the detailed interactions between components in the HearSee application for each use case. The diagrams show:

1. The flow of control between the user interface, application logic, and services
2. The precise method calls with parameters
3. Conditional logic for error handling and validation
4. The integration with external APIs (Replicate)
5. The data transformations that occur during processing