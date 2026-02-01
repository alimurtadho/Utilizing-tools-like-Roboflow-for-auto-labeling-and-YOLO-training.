Helmet Compliance & Occupancy Counting System (Phase 1)

This project aims to automate road safety monitoring by using AI to detect motorcycle helmet usage and occupant counts from video footage.
📌 Project Overview

Manual road safety observation is labor-intensive and difficult to scale. This system replaces manual counting with an automated AI solution capable of processing offline MP4 video files to measure compliance rates accurately.
🎯 Business Objectives

    Occupancy Counting: Automatically count all motorcycle riders and passengers.

    Compliance Monitoring: Measure helmet usage rates, including specific tracking for children.

    Unique Tracking: Provide non-duplicated counts of motorcycles and occupants using line-cross logic.

    Scalability: Support batch processing for locally stored MP4 files.

🛠 Features & Scope
In Scope

    Object Detection: Development of models to identify motorcycles, occupants, and helmets.

    Classification: Distinguishing between "helmet" and "no-helmet" for all occupants.

    Line-Crossing Logic: Unique counting triggered when a motorcycle crosses a virtual line in the ROI.

    Occupancy Handling: Evaluating all visible occupants regardless of count (including over-occupancy). 

Out of Scope

    Verification of helmet certifications (e.g., SNI).

    Enforcement features like License Plate Recognition (LPR).

    Modified motorcycles with large attachments. 

📊 Key Deliverables

    Trained Model: Optimized for helmet compliance detection.

    Counting System: Integration of line-cross logic for unique event recording.

    Guidelines: Comprehensive data recording and labeling documentation.

    Reporting: Exportable calculation results and compliance ratios. 

🚀 Implementation Strategy

The project prioritizes efficiency by minimizing "from-scratch" development:

    Managed Platforms: Utilizing tools like Roboflow for auto-labeling and YOLO training.

    Foundation Models: Leveraging pretrained models to generate initial annotations and reducing manual labor.

    Iterative Improvement: Fine-tuning the dataset through human correction to stabilize the workflow.

📅 Timeline (2026)

    February: Finalize guidelines and collect video data.

    March: Auto-labeling, manual correction, and model training.

    April: Video inference, counting execution, and final reporting. 

✅ Success Criteria

    Accurate helmet compliance rates across all occupants.

    Unique, non-duplicated counting via line-cross method.

    A scalable workflow for processing local MP4 files.

    Demonstrated ability to improve model performance through iterative labeling.