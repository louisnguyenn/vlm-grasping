## November 25, 2026

### Objectives

- Investigate accessible VLMs for direct robotic grasp prediction.
- Establish the initial development environment.
- Verify programmatic model access.
- Inspect the Cornell Grasping Dataset.

### Work Completed

- Investigated alternative VLMs due to the financial constraints associated with OpenAI Astra API access.
- Selected Google Gemini for preliminary experimentation.
- Established the `vlm-grasping` Git repository.
- Configured the Python virtual environment and API credentials.
- Successfully conducted a text-based Gemini inference test.
- Acquired and inspected the Cornell Grasping Dataset.
- Identified 896 RGB images and 885 positive grasp annotation files.
- Created an initial visual inference script.

### Key Findings

- Gemini can be accessed programmatically through the Python SDK.
- The Cornell dataset provides annotated grasp rectangles suitable for quantitative evaluation.
- The dataset contains both RGB and depth information, supporting subsequent research stages.
- Dataset pairing and validation are required before automated experimentation.

### Technical Decisions

- Utilize Gemini as a provisional VLM for initial experimentation.
- Maintain a model-independent software architecture.
- Utilize RGB images exclusively during Step 1.
- Reserve ground-truth grasp annotations for evaluation.
- Develop a reusable dataset loader to support automated experimentation.

### Challenges

- API costs associated with the initially proposed OpenAI model.
- Potential free-tier API rate limitations.
- Unequal numbers of RGB images and positive annotation files.

### Next Steps

- Implement and validate the Cornell dataset loader.
- Conduct the first image-based inference experiment.
- Evaluate qualitative grasp reasoning.
- Investigate numerical grasp prediction.
- Coordinate the grasp output format with Zichen.
