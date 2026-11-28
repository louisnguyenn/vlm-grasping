## November 28, 2026

### Preliminary Experiment — Direct VLM-Based Grasp Prediction

**Objective**

Investigate the ability of a general-purpose vision-language model to interpret an RGB image and independently generate a robotic grasping solution using a basic natural language prompt.

**Experimental Configuration**

| Parameter | Value |
|---|---|
| Model | Gemini 3.6 Flash (`gemini-3.6-flash`) |
| Dataset | Cornell Grasping Dataset |
| Sample ID | pcd0100 |
| Image resolution | 640 × 480 pixels |
| Input modality | RGB image and natural language |
| Prompting strategy | Basic zero-shot prompting |
| Gripper configuration | Top-down parallel-jaw gripper |

**Methodology**

An RGB image from the Cornell Grasping Dataset was provided to Gemini alongside a natural language instruction requesting object identification, grasp location, grasp orientation and justification of the proposed grasp.

No ground-truth grasp annotations, explicit coordinate conventions or structured output requirements were provided to the model.

**Results**

The model identified the object as a black remote control and independently generated numerical grasp parameters using a normalized 1000 × 1000 coordinate system.

| Parameter | Model prediction |
|---|---|
| Identified object | Black remote control |
| Normalized grasp centre (y, x) | (638, 442) |
| Converted grasp centre (x, y) | (282.88, 306.24) pixels |
| Grasp orientation | 85°–90° |
| Gripper opening width | 65–75 normalized units |
| Request latency | 144.42 seconds |

The model justified its prediction by considering the estimated centre of mass, available contact surfaces and potential collision risks.

**Key Findings**

- Gemini successfully processed combined visual and natural language inputs.
- The model independently generated numerical spatial information without explicit instructions to return coordinates.
- The model demonstrated qualitative reasoning relevant to robotic grasp planning.
- The model utilized normalized coordinates rather than the original image coordinate system.
- Grasp orientation and opening width were expressed as ranges rather than deterministic numerical values.

**Identified Limitations**

- The output was not provided in a standardized, machine-readable format.
- Coordinate ordering and geometric conventions require explicit definition.
- The grasp rectangle height was not provided.
- The observed inference latency was relatively high for potential real-time robotic applications.
- Object recognition and grasp prediction accuracy have not yet been independently verified against the original image and ground-truth annotations.
- Physical grasp stability cannot be established from the model's response alone.

**Next Steps**

- Visualize the predicted grasp centre on the original RGB image.
- Develop structured prompts with explicit coordinate and geometric conventions.
- Investigate JSON-based grasp prediction outputs.
- Compare predicted grasp rectangles against Cornell ground-truth annotations.
- Collect additional inference latency measurements.
- Evaluate the effect of different prompting strategies on prediction accuracy and consistency.

**Preliminary Conclusion**

The initial experiment demonstrates the feasibility of obtaining numerical grasp predictions directly from a general-purpose vision-language model. However, further prompt engineering, output standardization and quantitative evaluation are required before determining the reliability of this approach for robotic grasping applications.

### Experiment 2 — Structured Prompting and Spatial Localization

**Objective**

Investigate whether explicit coordinate conventions and structured output requirements improve the usability and accuracy of VLM-generated robotic grasp predictions.

**Experimental Configuration**

- Model: Gemini 3.6 Flash (`gemini-3.6-flash`)
- Dataset: Cornell Grasping Dataset
- Sample: pcd0100
- Object: Remote control
- Image resolution: 640 × 480 pixels
- Prompting strategies: Basic zero-shot prompting and structured zero-shot prompting

**Experimental Results**

| Parameter | Basic Prompt | Structured Prompt |
|---|---|---|
| Object recognition | Correct | Correct |
| Grasp centre (pixels) | (282.88, 306.24) | (442, 306) |
| Grasp orientation | 85°–90° | 3° |
| Gripper width | 65–75 normalized units | 65 pixels |
| Rectangle height | Not provided | 30 pixels |
| Output format | Unstructured Markdown | JSON within Markdown code fence |
| Request latency | 144.42 s | 16.96 s |
| Visual centre localization | On target | Outside target |

**Observations**

Visualization of the initial prediction confirmed that the predicted grasp centre was located approximately at the geometric centre of the remote control.

The structured prompt successfully produced a consistent set of numerical parameters in a JSON-formatted response. However, the predicted grasp centre was located outside the target object, resulting in an unsuitable grasp location.

A comparison of the two predictions revealed that the structured prediction retained the previous normalized x-coordinate while producing a y-coordinate approximately equal to the converted pixel coordinate.

This suggests a potential inconsistency in the model's interpretation or conversion of spatial coordinates.

**Key Findings**

- Explicit output formatting does not necessarily improve spatial localization accuracy.
- Structured prompting successfully improved the machine readability of the model response.
- The model may exhibit inconsistencies when converting normalized spatial coordinates into image pixel coordinates.
- The structured prediction demonstrated an observed latency reduction of approximately 88.3%, although additional trials are required to establish a reliable comparison.
- Qualitative grasp reasoning does not necessarily correspond to accurate numerical grasp predictions.

**Proposed Methodological Improvement**

To reduce potential coordinate conversion inconsistencies, subsequent experiments will investigate normalized spatial predictions with deterministic coordinate conversion performed externally in Python.

Additionally, a contact-point-based grasp representation will be investigated. The model will predict opposing gripper contact points, from which grasp centre, contact separation and orientation can be calculated mathematically.

This approach aims to reduce reliance on the VLM for deterministic geometric calculations.

**Limitations**

The observations are based on a single image and one inference trial per prompting strategy. Quantitative comparison against ground-truth grasp rectangles has not yet been performed.

**Preliminary Conclusion**

The experiment demonstrates that structured prompting can improve output standardization without necessarily improving spatial prediction accuracy. Further investigation is required to determine whether normalized coordinate representations and contact-point-based predictions improve grasp localization and consistency.

### Experiment 3 — Normalized Contact-Point-Based Grasp Prediction

**Objective**

Investigate whether normalized spatial coordinates and external geometric calculations can improve the localization accuracy, geometric consistency and usability of VLM-generated grasp predictions.

**Hypothesis**

Delegating coordinate conversion and geometric calculations to deterministic software, rather than relying on the VLM to directly estimate pixel-based grasp parameters, may improve prediction reliability.

**Experimental Configuration**

| Parameter | Value |
|---|---|
| Model | Gemini 3.6 Flash |
| Dataset | Cornell Grasping Dataset |
| Sample ID | pcd0100 |
| Image resolution | 640 × 480 pixels |
| Object | Remote control |
| Prompting strategy | Structured normalized contact-point prompting |
| Coordinate representation | Normalized 0–1000 |

**Methodology**

The model was instructed to identify a suitable grasp centre and two opposing gripper contact points using normalized image coordinates. The model was explicitly instructed not to perform pixel coordinate conversion.

The predicted contact points were subsequently converted into pixel coordinates. Grasp centre, contact separation and orientation were calculated mathematically from the converted contact points.

**Results**

| Parameter | Normalized prediction | Pixel coordinates |
|---|---|---|
| Grasp centre | (440, 638) | (281.60, 306.24) |
| Contact point 1 | (409, 638) | (261.76, 306.24) |
| Contact point 2 | (471, 638) | (301.44, 306.24) |

Calculated grasp parameters:

- Grasp centre: (281.60, 306.24) pixels.
- Contact separation: 39.68 pixels.
- Gripper closing orientation: 0°.
- Centre consistency error: 0.00 pixels.
- API request latency: 13.56 seconds.

**Key Findings**

- The model successfully generated structured normalized spatial coordinates.
- The predicted grasp centre differed from the initial visually verified baseline prediction by only 1.28 pixels.
- The predicted grasp centre exactly matched the calculated midpoint of the opposing contact points.
- External geometric calculations eliminated the need for the model to independently estimate grasp orientation and contact separation.
- The normalized prediction avoided the apparent coordinate conversion inconsistency observed in the previous pixel-based experiment.
- The observed inference latency was approximately 90.6% lower than that of the initial basic prompting experiment.

**Limitations**

- Results are based on a single image and one inference trial per prompting strategy.
- The effects of coordinate normalization and contact-point representation have not yet been isolated.
- Contact-point accuracy has not yet been quantitatively evaluated.
- Contact separation does not necessarily represent the required initial gripper opening.
- Grasp rectangle height requires standardization before IoU evaluation.
- Physical grasp success has not been established.

**Preliminary Conclusion**

Normalized contact-point-based prompting demonstrates potential as an alternative to direct pixel-based grasp prediction. Combining VLM-based spatial reasoning with deterministic geometric calculations produced an internally consistent grasp representation for the tested sample.

Further experiments across multiple objects and repeated trials are required to determine whether this approach consistently improves grasp prediction performance.
