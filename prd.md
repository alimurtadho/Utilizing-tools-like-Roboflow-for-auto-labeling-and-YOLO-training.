# Product Requirements Document (PRD)
## Helmet Compliance & Occupancy Counting System - Phase 1

**Version:** 1.0  
**Date:** January 31, 2026  
**Project Code:** ASTRA-HC-001

---

## 1. Executive Summary

### 1.1 Product Vision
Automated AI-powered road safety monitoring system that detects motorcycle helmet usage and occupancy from video footage, enabling scalable compliance measurement and data-driven safety interventions.

### 1.2 Target Users
- Traffic Safety Officers
- Government Transportation Agencies
- Road Safety Researchers
- Urban Planning Departments

### 1.3 Value Proposition
Replace manual, labor-intensive road safety observations with automated AI analysis that provides accurate, scalable, and actionable compliance data from offline video footage.

---

## 2. Product Architecture

### 2.1 System Components

#### **Frontend Application**
- **Framework:** Next.js 14 (App Router)
- **UI Library:** Shadcn/ui + Tailwind CSS
- **Deployment:** Vercel (Free Tier)
- **Domain:** `*.vercel.app` (free subdomain)

#### **Backend API**
- **Framework:** Next.js API Routes / Python FastAPI
- **Deployment:** Vercel Serverless Functions (for Next.js) or Railway.app (for Python, free tier)
- **Storage:** Supabase (Free tier: 500MB database, 1GB file storage)

#### **AI/ML Pipeline**
- **Object Detection Model:** YOLOv8 (Ultralytics)
- **Model Training:** Roboflow (Free tier: 10k images, 3 models)
- **Inference:** 
  - **Free LLM for Analysis:** Google Gemini 1.5 Flash (Free tier: 15 RPM, 1M tokens/day)
  - **Vision API:** Google Gemini Pro Vision (Free: 60 requests/min)
- **Video Processing:** FFmpeg (open source)

#### **Data Storage**
- **Database:** Supabase PostgreSQL (Free: 500MB)
- **File Storage:** Supabase Storage (Free: 1GB)
- **Alternative:** Cloudflare R2 (Free: 10GB storage)

#### **Monitoring & Analytics**
- **Logging:** Vercel Analytics (Free)
- **Error Tracking:** Sentry (Free tier: 5k events/month)

---

## 3. Functional Requirements

### 3.1 Video Upload & Management

**FR-001: Video Upload Interface**
- Users can upload MP4 video files up to 100MB
- Support drag-and-drop interface
- Display upload progress bar
- Validate video format (MP4, MOV, AVI)

**FR-002: Video Library**
- List all uploaded videos with metadata
- Show processing status (Pending, Processing, Completed, Failed)
- Allow video deletion
- Display thumbnail preview

**FR-003: ROI Configuration**
- Web-based interface to draw virtual line for counting
- Preview first frame of video
- Save ROI coordinates to database
- Support multiple counting lines per video

### 3.2 Detection & Classification

**FR-004: Object Detection**
- Detect motorcycles with bounding boxes
- Identify all occupants on each motorcycle
- Detect helmets on each occupant
- Confidence score threshold: ≥ 70%

**FR-005: Classification**
- Classify each occupant as "helmet" or "no-helmet"
- Identify child occupants (size-based heuristic)
- Track occupancy count (rider + passengers)

**FR-006: Line-Crossing Logic**
- Trigger counting event when motorcycle crosses virtual line
- Assign unique ID to each motorcycle
- Prevent duplicate counting of same motorcycle
- Track direction of movement (optional)

### 3.3 Analysis & Reporting

**FR-007: Real-time Processing Status**
- WebSocket or polling-based status updates
- Progress indicator (frames processed / total frames)
- ETA calculation

**FR-008: Compliance Dashboard**
- Total motorcycles counted
- Helmet compliance rate (%)
- Breakdown by occupant type (rider vs passenger)
- Child helmet compliance rate
- Occupancy statistics (solo, duo, 3+)

**FR-009: Data Export**
- Export results as CSV/Excel
- Include timestamp, motorcycle ID, occupancy count, helmet status
- Generate PDF report with charts
- API endpoint for programmatic access

**FR-010: Video Playback with Annotations**
- Play processed video with bounding boxes
- Show helmet/no-helmet labels
- Display counting line and crossing events
- Adjustable playback speed

---

## 4. Non-Functional Requirements

### 4.1 Performance

**NFR-001: Video Processing Speed**
- Target: Process 30 FPS video at 2-5 FPS inference speed
- Max processing time: 10 minutes for 5-minute video
- Queue system for batch processing

**NFR-002: Response Time**
- Dashboard loading: < 2 seconds
- Video upload initiation: < 1 second
- API response time: < 500ms (excluding video processing)

### 4.2 Scalability

**NFR-003: Free Tier Constraints**
- Vercel: 100GB bandwidth/month, 6000 build minutes/month
- Supabase: 500MB database, 2GB bandwidth/month
- Gemini API: 15 requests/minute, 1M tokens/day

**NFR-004: Concurrent Processing**
- Support 3-5 concurrent users
- Queue system with max 10 jobs
- Job timeout: 15 minutes (Vercel serverless limit)

### 4.3 Security

**NFR-005: Authentication**
- Simple email/password authentication (Supabase Auth)
- JWT token-based API access
- Public sharing links with expiry (optional)

**NFR-006: Data Privacy**
- Videos automatically deleted after 30 days
- HTTPS encryption for all data transfer
- No video data sent to third parties except processing

### 4.4 Usability

**NFR-007: User Experience**
- Mobile-responsive design
- Intuitive drag-and-drop interface
- Clear error messages
- Progressive disclosure of advanced features

---

## 5. Technical Implementation Details

### 5.1 Free Deployment Stack

#### **Frontend (Vercel)**
```yaml
Platform: Vercel
Framework: Next.js 14
Domain: astra-helmet-detection.vercel.app (example)
Build: Automatic deployment from GitHub
Limits:
  - 100GB bandwidth/month
  - 100 serverless function invocations/hour
  - 10 second serverless timeout (hobby), 300s (enterprise)
```

#### **Backend Processing (Railway or Render)**
```yaml
Option 1 - Railway.app:
  - Free tier: 500 execution hours/month
  - Python FastAPI service
  - Background workers for video processing
  
Option 2 - Render.com:
  - Free tier: 750 hours/month
  - Auto-sleep after 15 min inactivity
  - Wake time: 30-60 seconds
```

#### **AI/ML Models**

**Free LLM Options:**
```yaml
Primary: Google Gemini 1.5 Flash
  - Free tier: 15 RPM, 1M tokens/day
  - Use case: Analyze detection results, generate insights
  - API: Google AI Studio (no credit card required)

Alternative: OpenRouter (Multiple Free Models)
  - Meta Llama 3.1 8B (Free)
  - Google Gemini Flash 1.5 (Free)
  - Mistral 7B (Free)

Vision API: Google Gemini Pro Vision
  - Free tier: 60 RPM
  - Use case: Initial frame analysis, verification
```

**Object Detection:**
```yaml
Model: YOLOv8n (nano - fastest)
Training: Roboflow (Free tier)
Inference: Local or HuggingFace Inference API
Pretrained: COCO weights + fine-tuning
Custom Classes:
  - motorcycle
  - person_on_motorcycle
  - helmet
  - no_helmet
```

#### **Storage**
```yaml
Primary: Supabase
  - Database: 500MB PostgreSQL
  - Storage: 1GB for videos/results
  - Bandwidth: 2GB/month
  
Alternative: Cloudflare R2
  - 10GB storage (free)
  - No egress fees
  - Use for larger video files
```

### 5.2 API Design

#### **Endpoints**

```
POST   /api/videos/upload
GET    /api/videos
GET    /api/videos/:id
DELETE /api/videos/:id
POST   /api/videos/:id/process
GET    /api/videos/:id/status
GET    /api/videos/:id/results
POST   /api/videos/:id/roi
GET    /api/analytics/summary
GET    /api/analytics/export
```

#### **Data Models**

```typescript
Video {
  id: string
  filename: string
  fileSize: number
  uploadedAt: timestamp
  status: enum (pending|processing|completed|failed)
  userId: string
  roiConfig: JSON
  processingProgress: number
}

Detection {
  id: string
  videoId: string
  frameNumber: number
  timestamp: number
  motorcycleId: string
  occupantCount: number
  helmetsDetected: number
  confidenceScore: number
  boundingBoxes: JSON
  isUniqueCrossing: boolean
}

Analytics {
  videoId: string
  totalMotorcycles: number
  totalOccupants: number
  helmetsWorn: number
  complianceRate: number
  childOccupants: number
  childComplianceRate: number
  occupancyDistribution: JSON
}
```

### 5.3 Video Processing Pipeline

```
1. Upload Video → Supabase Storage
2. Extract Metadata → Save to Database
3. Queue Processing Job → Background Worker
4. Extract Frames → FFmpeg (1 FPS or 5 FPS)
5. Run YOLOv8 Detection → Each Frame
6. Apply Tracking → ByteTrack or SORT
7. Line-Crossing Detection → Unique Count
8. Aggregate Results → Database
9. Generate Summary → Using Gemini API
10. Create Annotated Video → FFmpeg overlay
11. Update Status → Complete
```

### 5.4 Line-Crossing Algorithm

```python
class LineCrossingDetector:
    def __init__(self, line_start, line_end):
        self.line = (line_start, line_end)
        self.crossed_ids = set()
    
    def check_crossing(self, track_id, prev_pos, curr_pos):
        if self.crosses_line(prev_pos, curr_pos):
            if track_id not in self.crossed_ids:
                self.crossed_ids.add(track_id)
                return True  # Unique crossing
        return False
    
    def crosses_line(self, p1, p2):
        # Line intersection algorithm
        # Returns True if line segment p1-p2 crosses counting line
        pass
```

---

## 6. User Stories

### 6.1 Core Features

**US-001: Upload Video for Analysis**
```
As a traffic officer
I want to upload a video file from my computer
So that I can analyze motorcycle helmet compliance
```

**US-002: Define Counting Line**
```
As a traffic officer
I want to draw a virtual line on the video
So that motorcycles are counted only once when crossing
```

**US-003: View Compliance Results**
```
As a safety researcher
I want to see helmet compliance statistics
So that I can report on road safety metrics
```

**US-004: Export Data**
```
As a government analyst
I want to export detection results to Excel
So that I can include them in official reports
```

**US-005: Watch Annotated Video**
```
As a supervisor
I want to watch the processed video with bounding boxes
So that I can verify the AI detection accuracy
```

---

## 7. Implementation Roadmap

### Phase 1: MVP (Week 1-2)
- ✅ Setup Vercel + Next.js project
- ✅ Implement video upload UI (Supabase Storage)
- ✅ Basic YOLOv8 integration (pre-trained model)
- ✅ Simple ROI drawing interface
- ✅ Display detection results in table format

### Phase 2: Core Features (Week 3-4)
- ✅ Implement line-crossing logic
- ✅ Add object tracking (ByteTrack)
- ✅ Create analytics dashboard
- ✅ Generate compliance reports
- ✅ Export to CSV/PDF

### Phase 3: Fine-tuning (Week 5-6)
- ✅ Collect and label custom dataset (Roboflow)
- ✅ Train custom YOLOv8 model
- ✅ Improve helmet detection accuracy
- ✅ Add child occupant detection

### Phase 4: Enhancement (Week 7-8)
- ✅ Integrate Gemini API for insights generation
- ✅ Create annotated video output
- ✅ Batch processing support
- ✅ User authentication
- ✅ Mobile responsive UI

---

## 8. Free Tools & Services Setup

### 8.1 Required Accounts (All Free)

1. **Vercel** (vercel.com)
   - Sign up with GitHub
   - Import Next.js project
   - Auto-deploy on push

2. **Supabase** (supabase.com)
   - Create new project
   - Setup database schema
   - Enable Storage bucket
   - Copy API keys to `.env`

3. **Google AI Studio** (ai.google.dev)
   - Get Gemini API key
   - Free tier: 1M tokens/day
   - No credit card required

4. **Roboflow** (roboflow.com)
   - Create workspace
   - Upload training images
   - Auto-labeling with Roboflow 3.0
   - Export YOLOv8 format

5. **Railway.app** (railway.app) *Optional*
   - For background processing
   - Deploy Python FastAPI
   - Free 500 hours/month

### 8.2 Environment Configuration

```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

GOOGLE_GEMINI_API_KEY=your_gemini_key

ROBOFLOW_API_KEY=your_roboflow_key
ROBOFLOW_WORKSPACE=your_workspace
ROBOFLOW_PROJECT=helmet-detection

# Optional: For background processing
RAILWAY_API_URL=your_railway_service_url
```

### 8.3 Deployment Commands

```bash
# Install dependencies
npm install

# Run locally
npm run dev

# Deploy to Vercel
vercel --prod

# Or auto-deploy via GitHub integration
git push origin main
```

---

## 9. Testing Strategy

### 9.1 Test Scenarios

**TS-001: Video Upload**
- ✅ Upload valid MP4 file (< 100MB)
- ✅ Reject invalid file types
- ✅ Reject oversized files
- ✅ Display upload progress

**TS-002: Detection Accuracy**
- ✅ Detect motorcycle in clear visibility
- ✅ Detect helmets on all occupants
- ✅ Handle occlusion scenarios
- ✅ Test with varying lighting conditions

**TS-003: Line Crossing**
- ✅ Count motorcycle crossing from left to right
- ✅ Do not double-count same motorcycle
- ✅ Handle multiple motorcycles simultaneously

**TS-004: Compliance Calculation**
- ✅ Calculate correct compliance rate
- ✅ Separate rider and passenger statistics
- ✅ Identify child occupants correctly

### 9.2 Test Data

- Sample videos: 5-10 short clips (30 sec - 2 min)
- Variety: Day/night, clear/rainy, busy/light traffic
- Ground truth: Manually counted motorcycles and helmets

---

## 10. Success Metrics

### 10.1 Technical KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Detection Accuracy (mAP) | ≥ 75% | YOLOv8 validation |
| Precision (Helmet Detection) | ≥ 80% | Confusion matrix |
| Recall (Motorcycle Detection) | ≥ 85% | Against ground truth |
| False Positive Rate | ≤ 10% | Manual verification |
| Processing Speed | 2-5 FPS | Inference time |
| Unique Counting Accuracy | ≥ 90% | Against manual count |

### 10.2 User Experience KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Time to First Result | < 5 min | Upload to result display |
| Dashboard Load Time | < 2 sec | Lighthouse score |
| User Task Completion | ≥ 80% | Usability testing |
| Error Rate | < 5% | Sentry logs |

### 10.3 Business Impact

- **Cost Reduction:** 80% less manual labor vs traditional counting
- **Scalability:** Process 100+ videos per month (vs 10 manual)
- **Data Quality:** Consistent, reproducible measurements
- **Actionable Insights:** Real-time compliance trends

---

## 11. Risk Management

### 11.1 Technical Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Free tier limits exceeded | High | Implement rate limiting, usage monitoring |
| Model accuracy insufficient | High | Iterative dataset improvement, transfer learning |
| Video processing timeout (15min) | Medium | Chunk processing, external worker service |
| Storage quota exceeded | Medium | Auto-delete old videos, compression |

### 11.2 Operational Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Poor video quality (blur, dark) | High | Pre-processing filters, reject low quality |
| Complex traffic scenarios | Medium | Focus on controlled test cases first |
| False positives in counting | Medium | Tunable confidence threshold, manual review |
| User adoption challenges | Low | Simple UI, tutorial videos |

---

## 12. Future Enhancements (Phase 2+)

### 12.1 Advanced Features
- Real-time RTSP camera stream processing
- License plate recognition (LPR) integration
- Multi-camera synchronization
- Helmet type classification (full-face, half, etc.)
- Weather condition detection and filtering

### 12.2 Paid Tier Migration
- Upgrade to Vercel Pro for longer execution time
- Dedicated GPU inference (RunPod, Vast.ai)
- Higher resolution model (YOLOv8m or YOLOv8l)
- Custom domain with SSL
- Advanced analytics and reporting

---

## 13. Documentation Requirements

### 13.1 User Documentation
- ✅ Getting Started Guide
- ✅ Video Upload Tutorial
- ✅ ROI Configuration Guide
- ✅ Interpreting Results
- ✅ FAQ and Troubleshooting

### 13.2 Technical Documentation
- ✅ API Reference
- ✅ Database Schema
- ✅ Model Training Guide
- ✅ Deployment Instructions
- ✅ Development Setup

### 13.3 Training Materials
- ✅ Video tutorial (5-10 min)
- ✅ Sample datasets
- ✅ Best practices guide

---

## 14. Compliance & Ethics

### 14.1 Data Privacy
- Videos stored temporarily (30-day auto-deletion)
- No personally identifiable information (PII) collected
- GDPR-compliant data handling
- User consent for video processing

### 14.2 Ethical Considerations
- System for monitoring safety, not punishment
- Transparent methodology and limitations
- Human oversight recommended for decisions
- Bias testing across demographics

---

## 15. Appendix

### 15.1 Technology Stack Summary

```yaml
Frontend:
  - Next.js 14 (App Router)
  - TypeScript
  - Shadcn/ui + Tailwind CSS
  - Recharts (data visualization)

Backend:
  - Next.js API Routes
  - Python FastAPI (optional for heavy processing)

AI/ML:
  - YOLOv8 (Ultralytics)
  - Google Gemini 1.5 Flash
  - ByteTrack (object tracking)
  - OpenCV + FFmpeg

Database & Storage:
  - Supabase (PostgreSQL + Storage)
  - Prisma ORM

Deployment:
  - Vercel (frontend + serverless)
  - Railway/Render (background workers)
  - GitHub Actions (CI/CD)

Monitoring:
  - Vercel Analytics
  - Sentry (error tracking)
```

### 15.2 Cost Estimate (Free Tier)

| Service | Free Limit | Estimated Usage | Status |
|---------|-----------|-----------------|--------|
| Vercel | 100GB bandwidth | ~20GB/month | ✅ Safe |
| Supabase | 500MB DB, 1GB storage | ~800MB total | ⚠️ Monitor |
| Gemini API | 1M tokens/day | ~50k tokens/day | ✅ Safe |
| Railway | 500 hours/month | ~200 hours/month | ✅ Safe |
| Roboflow | 10k images | ~5k images | ✅ Safe |

**Total Monthly Cost: $0** (within free tiers)

### 15.3 Upgrade Path

When usage grows:
- Vercel Pro: $20/month (longer execution, team features)
- Supabase Pro: $25/month (8GB database, 100GB storage)
- Gemini API Pay-as-you-go: ~$0.10 per 1M tokens
- Railway Pro: $5/month base + usage

Estimated cost at scale: **$30-50/month** for 1000+ videos

---

## 16. Approval & Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | | | |
| Technical Lead | | | |
| Stakeholder | | | |

---

**Document Control:**
- Version: 1.0
- Last Updated: January 31, 2026
- Next Review: February 15, 2026
- Status: Draft → Ready for Implementation

