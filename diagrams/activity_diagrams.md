# HearSee Application - UML Activity Diagrams

This document contains UML activity diagrams for the key workflows in the HearSee application, a multimodal chat application with vision and voice capabilities.

## Table of Contents

1. [Image Upload Workflow](#image-upload-workflow)
2. [Chat Interaction Workflow](#chat-interaction-workflow)
3. [Text Extraction Workflow](#text-extraction-workflow)
4. [Image Captioning Workflow](#image-captioning-workflow)
5. [Image Summarization Workflow](#image-summarization-workflow)
6. [Text-to-Speech Conversion Workflow](#text-to-speech-conversion-workflow)

## Image Upload Workflow

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> ClickUpload[Click 'Upload Image' button]
        SelectImage[Select image file] --> WaitForProcessing[Wait for processing]
    end
    
    subgraph UI
        ClickUpload --> ShowFileDialog[Show file selection dialog]
        ShowFileDialog --> SelectImage
        WaitForProcessing --> DisplayImage[Display image in gallery]
        DisplayImage --> EnableButtons[Enable interaction buttons]
    end
    
    subgraph System
        EnableButtons --> ValidateImage{Validate image}
        ValidateImage -->|Valid| StoreImage[Store image in memory]
        ValidateImage -->|Invalid| ShowError[Show error message]
        StoreImage --> UpdateUIState[Update UI state]
        ShowError --> End([End])
    end
    
    UpdateUIState --> End
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Upload limited to 10MB]:::note
    Note2[Buttons enabled: Send, Extract Text, Caption, Summarize]:::note
    
    ValidateImage -.-> Note1
    EnableButtons -.-> Note2
```

## Chat Interaction Workflow

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> ImageUploaded{Image uploaded?}
        ImageUploaded -->|No| UploadImage[Upload image first]
        ImageUploaded -->|Yes| EnterMessage[Enter message in text field]
        EnterMessage --> SendMessage[Click 'Send' or press Enter]
        WaitForResponse[Wait for AI response] --> ViewResponse[View AI response]
        ViewResponse --> Decision{Continue conversation?}
        Decision -->|Yes| EnterMessage
        Decision -->|No| End([End])
    end
    
    subgraph UI
        SendMessage --> ShowProcessing[Show processing indicator]
        ShowProcessing --> DisableInteraction[Disable interactive elements]
        ProcessingComplete[Processing complete] --> EnableInteraction[Re-enable interactive elements]
        EnableInteraction --> DisplayResponse[Display response in chat]
        DisplayResponse --> UpdateMetrics[Update performance metrics]
    end
    
    subgraph System
        DisableInteraction --> ValidateInputs{Validate inputs}
        ValidateInputs -->|Invalid| ShowError[Show error message]
        ValidateInputs -->|Valid| CheckAPI{Check API availability}
        CheckAPI -->|Unavailable| APIError[Show API error]
        CheckAPI -->|Available| ProcessMessage[Process message with vision model]
        ProcessMessage --> GenerateResponse[Generate AI response]
        GenerateResponse --> ProcessingComplete
        ShowError --> EnableInteraction
        APIError --> EnableInteraction
    end
    
    UploadImage --> Start
    UpdateMetrics --> WaitForResponse
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Send button disabled until image uploaded]:::note
    Note2[Uses Qwen VL model via Replicate API]:::note
    Note3[Metrics include latency and word count]:::note
    
    ImageUploaded -.-> Note1
    ProcessMessage -.-> Note2
    UpdateMetrics -.-> Note3
```

## Text Extraction Workflow

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> ImageUploaded{Image uploaded?}
        ImageUploaded -->|No| UploadImage[Upload image first]
        ImageUploaded -->|Yes| ClickExtract[Click 'Extract Text' button]
        WaitForProcessing[Wait for processing] --> ViewResults[View extracted text]
        ViewResults --> End([End])
    end
    
    subgraph UI
        ClickExtract --> ShowProcessing[Show processing indicator]
        ShowProcessing --> DisableInteraction[Disable interactive elements]
        ProcessingComplete[Processing complete] --> EnableInteraction[Re-enable interactive elements]
        EnableInteraction --> DisplayResults[Display extracted text in chat]
        DisplayResults --> UpdateMetrics[Update performance metrics]
    end
    
    subgraph System
        DisableInteraction --> ValidateImage{Validate image}
        ValidateImage -->|Invalid| ShowError[Show error message]
        ValidateImage -->|Valid| ConvertImage[Convert image to base64]
        ConvertImage --> CheckAPI{Check API availability}
        CheckAPI -->|Unavailable| APIError[Show API error]
        CheckAPI -->|Available| CallVisionModel[Call vision model with OCR prompt]
        CallVisionModel --> ExtractText[Extract text from image]
        ExtractText --> ProcessingComplete
        ShowError --> EnableInteraction
        APIError --> EnableInteraction
    end
    
    UploadImage --> Start
    UpdateMetrics --> WaitForProcessing
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Extract Text button disabled until image uploaded]:::note
    Note2[Uses specialized prompt for OCR functionality]:::note
    Note3[Handles various text formats and layouts]:::note
    
    ImageUploaded -.-> Note1
    CallVisionModel -.-> Note2
    ExtractText -.-> Note3
```

## Image Captioning Workflow

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> ImageUploaded{Image uploaded?}
        ImageUploaded -->|No| UploadImage[Upload image first]
        ImageUploaded -->|Yes| ClickCaption[Click 'Caption Image' button]
        WaitForProcessing[Wait for processing] --> ViewCaption[View image caption]
        ViewCaption --> End([End])
    end
    
    subgraph UI
        ClickCaption --> ShowProcessing[Show processing indicator]
        ShowProcessing --> DisableInteraction[Disable interactive elements]
        ProcessingComplete[Processing complete] --> EnableInteraction[Re-enable interactive elements]
        EnableInteraction --> DisplayCaption[Display caption in chat]
        DisplayCaption --> UpdateMetrics[Update performance metrics]
    end
    
    subgraph System
        DisableInteraction --> ValidateImage{Validate image}
        ValidateImage -->|Invalid| ShowError[Show error message]
        ValidateImage -->|Valid| ConvertImage[Convert image to base64]
        ConvertImage --> CheckAPI{Check API availability}
        CheckAPI -->|Unavailable| APIError[Show API error]
        CheckAPI -->|Available| CallVisionModel[Call vision model with caption prompt]
        CallVisionModel --> GenerateCaption[Generate detailed image description]
        GenerateCaption --> ProcessingComplete
        ShowError --> EnableInteraction
        APIError --> EnableInteraction
    end
    
    UploadImage --> Start
    UpdateMetrics --> WaitForProcessing
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Caption button disabled until image uploaded]:::note
    Note2[Uses specialized prompt for detailed description]:::note
    Note3[Focuses on objects, people, scenery, colors, and composition]:::note
    
    ImageUploaded -.-> Note1
    CallVisionModel -.-> Note2
    GenerateCaption -.-> Note3
```

## Image Summarization Workflow

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> ImageUploaded{Image uploaded?}
        ImageUploaded -->|No| UploadImage[Upload image first]
        ImageUploaded -->|Yes| ClickSummarize[Click 'Summarize Image' button]
        WaitForProcessing[Wait for processing] --> ViewSummary[View image summary]
        ViewSummary --> End([End])
    end
    
    subgraph UI
        ClickSummarize --> ShowProcessing[Show processing indicator]
        ShowProcessing --> DisableInteraction[Disable interactive elements]
        ProcessingComplete[Processing complete] --> EnableInteraction[Re-enable interactive elements]
        EnableInteraction --> DisplaySummary[Display summary in chat]
        DisplaySummary --> UpdateMetrics[Update performance metrics]
    end
    
    subgraph System
        DisableInteraction --> ValidateImage{Validate image}
        ValidateImage -->|Invalid| ShowError[Show error message]
        ValidateImage -->|Valid| ConvertImage[Convert image to base64]
        ConvertImage --> CheckAPI{Check API availability}
        CheckAPI -->|Unavailable| APIError[Show API error]
        CheckAPI -->|Available| CallVisionModel[Call vision model with summary prompt]
        CallVisionModel --> GenerateSummary[Generate comprehensive contextual summary]
        GenerateSummary --> ProcessingComplete
        ShowError --> EnableInteraction
        APIError --> EnableInteraction
    end
    
    UploadImage --> Start
    UpdateMetrics --> WaitForProcessing
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Summarize button disabled until image uploaded]:::note
    Note2[More comprehensive than caption]:::note
    Note3[Includes context, analysis, and interpretation]:::note
    
    ImageUploaded -.-> Note1
    CallVisionModel -.-> Note2
    GenerateSummary -.-> Note3
```

## Text-to-Speech Conversion Workflow

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> ChatHistory{Chat history exists?}
        ChatHistory -->|No| NoAction[No action possible]
        ChatHistory -->|Yes| SelectVoice[Select voice type]
        SelectVoice --> AdjustSpeed[Adjust speech speed]
        AdjustSpeed --> ClickTTS[Click 'Play Last Response' button]
        WaitForProcessing[Wait for processing] --> ListenAudio[Listen to audio]
        ListenAudio --> End([End])
    end
    
    subgraph UI
        ClickTTS --> ShowProcessing[Show processing indicator]
        ShowProcessing --> DisableInteraction[Disable interactive elements]
        ProcessingComplete[Processing complete] --> EnableInteraction[Re-enable interactive elements]
        EnableInteraction --> DisplayAudio[Display audio player]
        DisplayAudio --> UpdateStatus[Update TTS status]
    end
    
    subgraph System
        DisableInteraction --> ValidateText{Validate text}
        ValidateText -->|Invalid| ShowError[Show error message]
        ValidateText -->|Valid| ValidateVoice[Validate voice type]
        ValidateVoice --> ValidateSpeed[Validate speed]
        ValidateSpeed --> CheckAPI{Check API availability}
        CheckAPI -->|Unavailable| APIError[Show API error]
        CheckAPI -->|Available| CallTTSModel[Call TTS model]
        CallTTSModel --> GenerateAudio[Generate audio file]
        GenerateAudio --> DownloadAudio[Download audio file]
        DownloadAudio --> CreateTempFile[Create temporary audio file]
        CreateTempFile --> ProcessingComplete
        ShowError --> EnableInteraction
        APIError --> EnableInteraction
    end
    
    NoAction --> End([End])
    UpdateStatus --> WaitForProcessing
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Voice options: Male/Female with different accents]:::note
    Note2[Speed range: 0.5x to 2.0x]:::note
    Note3[Uses Kokoro TTS model via Replicate API]:::note
    Note4[Temporary audio file created for playback]:::note
    
    SelectVoice -.-> Note1
    AdjustSpeed -.-> Note2
    CallTTSModel -.-> Note3
    CreateTempFile -.-> Note4
```

## Regenerate Response Workflow

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> ChatHistory{Chat history exists?}
        ChatHistory -->|No| NoAction[No action possible]
        ChatHistory -->|Yes| ClickRegenerate[Click 'Regenerate' button]
        WaitForProcessing[Wait for processing] --> ViewNewResponse[View new AI response]
        ViewNewResponse --> End([End])
    end
    
    subgraph UI
        ClickRegenerate --> ShowProcessing[Show processing indicator]
        ShowProcessing --> DisableInteraction[Disable interactive elements]
        ProcessingComplete[Processing complete] --> EnableInteraction[Re-enable interactive elements]
        EnableInteraction --> DisplayNewResponse[Display new response in chat]
        DisplayNewResponse --> UpdateMetrics[Update performance metrics]
    end
    
    subgraph System
        DisableInteraction --> ExtractLastMessage[Extract last user message]
        ExtractLastMessage --> RemoveLastPair[Remove last conversation pair]
        RemoveLastPair --> CheckAPI{Check API availability}
        CheckAPI -->|Unavailable| APIError[Show API error]
        CheckAPI -->|Available| ProcessMessage[Process message with vision model]
        ProcessMessage --> GenerateNewResponse[Generate new AI response]
        GenerateNewResponse --> ProcessingComplete
        APIError --> EnableInteraction
    end
    
    NoAction --> End([End])
    UpdateMetrics --> WaitForProcessing
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Regenerates response to the last user message]:::note
    Note2[Uses same image but may produce different response]:::note
    Note3[Preserves conversation history except last pair]:::note
    
    ClickRegenerate -.-> Note1
    ProcessMessage -.-> Note2
    RemoveLastPair -.-> Note3
```

## Clear History Workflow

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> ClickClear[Click 'Clear History' button]
        ViewReset[View reset interface] --> End([End])
    end
    
    subgraph UI
        ClickClear --> ResetChatbot[Reset chatbot to initial state]
        ResetChatbot --> ClearGallery[Clear image gallery]
        ClearGallery --> ResetMetrics[Reset performance metrics]
        ResetMetrics --> DisableButtons[Disable interaction buttons]
        DisableButtons --> ShowInstruction[Show image upload instruction]
    end
    
    subgraph System
        ShowInstruction --> ResetImageState[Reset image uploaded state]
        ResetImageState --> ClearImageData[Clear image data from memory]
        ClearImageData --> ResetProcessingState[Reset processing state]
    end
    
    ResetProcessingState --> ViewReset
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Completely resets the application state]:::note
    Note2[User must upload a new image to continue]:::note
    
    ClickClear -.-> Note1
    ShowInstruction -.-> Note2
```

## Exception Handling Workflow

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph User
        Start([Start]) --> UserAction[Perform any action]
        ViewError[View error message] --> RetryOption{Retry?}
        RetryOption -->|Yes| UserAction
        RetryOption -->|No| End([End])
    end
    
    subgraph System
        UserAction --> ProcessAction[Process user action]
        ProcessAction --> ExceptionOccurs{Exception occurs?}
        ExceptionOccurs -->|No| CompleteAction[Complete action normally]
        ExceptionOccurs -->|Yes| LogError[Log error details]
        LogError --> DetermineErrorType{Determine error type}
    end
    
    subgraph ErrorHandling
        DetermineErrorType -->|API Error| HandleAPIError[Handle API unavailability]
        DetermineErrorType -->|Image Error| HandleImageError[Handle image processing error]
        DetermineErrorType -->|Model Error| HandleModelError[Handle model execution error]
        DetermineErrorType -->|Other Error| HandleGenericError[Handle generic error]
        
        HandleAPIError --> FormatAPIError[Format API error message]
        HandleImageError --> FormatImageError[Format image error message]
        HandleModelError --> FormatModelError[Format model error message]
        HandleGenericError --> FormatGenericError[Format generic error message]
        
        FormatAPIError --> DisplayError[Display error to user]
        FormatImageError --> DisplayError
        FormatModelError --> DisplayError
        FormatGenericError --> DisplayError
    end
    
    CompleteAction --> End([End])
    DisplayError --> ViewError
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[All errors are logged with details]:::note
    Note2[User-friendly messages hide technical details]:::note
    Note3[System remains in usable state after errors]:::note
    
    LogError -.-> Note1
    DisplayError -.-> Note2
    DisplayError -.-> Note3
```

## System Startup Workflow

```mermaid
flowchart TD
    %% Define swimlanes
    subgraph System
        Start([Start]) --> LoadEnvironment[Load environment variables]
        LoadEnvironment --> ConfigureLogging[Configure logging]
        ConfigureLogging --> CreateTheme[Create custom UI theme]
        CreateTheme --> InitializeBlocks[Initialize Gradio Blocks]
        InitializeBlocks --> CreateTabs[Create Chat and Guide tabs]
    end
    
    subgraph ChatTab
        CreateTabs --> CreateChatInterface[Create chat interface components]
        CreateChatInterface --> SetupEventHandlers[Setup event handlers]
        SetupEventHandlers --> ConnectComponents[Connect UI components]
    end
    
    subgraph GuideTab
        CreateTabs --> CreateGuideInterface[Create guide interface]
    end
    
    subgraph Initialization
        ConnectComponents --> ReturnApp[Return app instance]
        CreateGuideInterface --> ReturnApp
        ReturnApp --> LaunchApp[Launch Gradio app]
        LaunchApp --> End([End])
    end
    
    %% Add notes
    classDef note fill:#ffffcc,stroke:#999,stroke-width:1px
    
    Note1[Loads API keys from .env file]:::note
    Note2[Sets up error logging and monitoring]:::note
    Note3[Creates responsive UI with light theme]:::note
    Note4[Launches in browser automatically]:::note
    
    LoadEnvironment -.-> Note1
    ConfigureLogging -.-> Note2
    CreateTheme -.-> Note3
    LaunchApp -.-> Note4
```

These activity diagrams provide a comprehensive visualization of all key workflows in the HearSee application, including both happy paths and exception handling. The diagrams use consistent notation throughout and clearly represent the system boundaries and actor responsibilities through swimlanes.