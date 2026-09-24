# LectureBridge AI - 7-Day Thai Learning Plan

เป้าหมายของเอกสารนี้คือทำให้คุณเริ่ม repo ของตัวเองได้แบบ engineer จริง: คิด problem, design, trade-off, implementation path, testing, deployment, demo, และ interview story ไม่ใช่แค่ clone repo แล้วเปลี่ยนชื่อโปรเจกต์

โปรเจกต์: **LectureBridge AI**

Concept: **Understand any lectures, docs, videos in your language**

MVP scope สำหรับ 1 สัปดาห์:

- สร้าง lecture workspace
- multi-upload สำหรับ `PDF`, `PPTX`, `TXT`, `VTT`
- แปลงไฟล์เป็น Canonical Document (เอกสารกลาง)
- แปล lecture เป็น Mandarin/Thai โดยรักษา academic terminology (ศัพท์วิชาการ)
- สรุป lecture note แบบมี structure
- ถามตอบจากเนื้อหา lecture ด้วย RAG (Retrieval-Augmented Generation / การดึงข้อมูลก่อนให้ AI ตอบ)
- มี source citation (อ้างอิงที่มา) เช่น file, page, slide, timestamp
- สร้าง review activities เช่น quiz, flashcards, concept comparison
- deploy web app แบบ demo ได้

สิ่งที่ยังไม่ควรทำใน MVP:

- auto-download protected YouTube/Coursera/Echo360 content
- production-scale live translation
- voice cloning
- payment
- LMS integration
- multi-agent architecture ถ้ายังไม่มีเหตุจำเป็น

เหตุผล: ถ้าทำทุกอย่างพร้อมกัน คุณจะได้ demo กว้างแต่ไม่ลึก สำหรับ portfolio/interview ใน Sydney/Australia คุณต้องโชว์ว่า “ผมสร้าง AI system ที่ traceable, testable, deployable ได้” มากกว่า “ผมต่อ API ได้”

## 1. Career Target

### Software Engineer (วิศวกรซอฟต์แวร์)

หน้าที่หลักคือออกแบบและสร้างระบบที่ maintainable (ดูแลต่อได้), reliable (เชื่อถือได้), secure (ปลอดภัย), testable (ทดสอบได้), และ deployable (ปล่อยใช้งานได้)

ในโปรเจกต์นี้ skill ที่ต้องโชว์:

- API design (ออกแบบ API)
- domain modeling (ออกแบบโมเดลธุรกิจ)
- database design (ออกแบบฐานข้อมูล)
- async processing (งานเบื้องหลัง)
- error handling (จัดการ error)
- tests (unit/integration/e2e)
- deployment (ปล่อยระบบ)
- observability (การมองเห็นระบบตอนรันจริง)

### AI Engineer (วิศวกร AI)

ในตลาดงานปัจจุบัน AI Engineer ไม่ได้แปลว่าต้อง train foundation model เองเสมอไป แต่คือคนที่เอา AI model เข้าไปอยู่ใน product ได้จริง

ต้องเข้าใจ:

- LLM (Large Language Model / โมเดลภาษาใหญ่)
- embeddings (เวกเตอร์แทนความหมาย)
- vector search (ค้นหาด้วยความใกล้เชิงความหมาย)
- RAG (ดึงข้อมูลก่อนตอบ)
- prompt design (ออกแบบคำสั่งให้โมเดล)
- evals (การวัดคุณภาพ AI)
- latency/cost trade-off (แลกความเร็วกับค่าใช้จ่าย)
- hallucination control (ลดการตอบมั่ว)
- privacy/security (ความเป็นส่วนตัวและความปลอดภัย)

### FDE - Forward Deployed Engineer (วิศวกรที่ลงไปแก้ปัญหาหน้างาน)

FDE mindset คือคุณไม่เริ่มจาก “ผมจะสร้าง chatbot” แต่เริ่มจาก:

- user คือใคร
- pain จริงคืออะไร
- workflow เดิมเป็นอย่างไร
- ข้อมูลเข้ามาทางไหน
- success metric คืออะไร
- อะไรต้อง trace ได้
- อะไรพังแล้ว user จะเสียหาย

สำหรับ LectureBridge AI ปัญหาจริงไม่ใช่ “แปลภาษา” อย่างเดียว แต่คือ:

- นักเรียนเข้าใจ lecture ไม่ทัน
- technical terms แปลไม่ consistent
- สรุปอ่านแล้วไม่มี source
- วิดีโอ/slide/PDF แยกกันเกินไป
- ก่อนสอบอยาก review แบบตรงกับเนื้อหา

คำตอบแบบ FDE:

> ผมจะเริ่มจาก uploaded lecture materials ก่อน เพราะมันควบคุมคุณภาพ input, citation, cost, และ privacy ได้ง่ายกว่า live translation จากนั้นค่อยเพิ่ม real-time audio เมื่อ document workflow มี eval และ user trust แล้ว

## 2. Product Thinking

### North Star

นักเรียนควรสามารถอัปโหลดเนื้อหา lecture แล้วได้คำตอบในภาษาที่ถนัด โดยยังเชื่อกลับไปที่ source ได้

### MVP User Story

As an international student,
I want to upload my lecture slides, subtitles, and notes,
so that I can read translated notes, ask questions, and review concepts in Thai or Mandarin with source citations.

### Success Metrics

- translation consistency: technical terms สำคัญแปลเหมือนกันอย่างน้อย 90% ในชุดทดสอบ
- citation accuracy: คำตอบ Q&A ต้องมี source ที่ถูกต้องอย่างน้อย 80% ใน eval set
- groundedness: ถ้าเอกสารไม่มีข้อมูล ระบบต้องตอบว่าไม่พบ evidence
- latency: Q&A ปกติควรตอบภายใน 8 seconds P95 สำหรับ MVP
- cost: ไม่ส่งทั้ง lecture เข้า LLM ทุกครั้ง ใช้ retrieval/chunking

### User Trust Rules

- AI ต้องบอกว่าอ้างจากไฟล์ไหน หน้าไหน slide ไหน หรือ timestamp ไหน
- ถ้าไม่พบข้อมูล ห้ามแต่งคำตอบ
- ถ้าแปลศัพท์วิชาการ ควรเก็บ glossary (อภิธานศัพท์) ต่อ lecture
- user ต้องรู้ว่าไฟล์ถูก upload แล้วถูก process สถานะอะไร

## 3. Legal And Platform Boundaries

YouTube, Coursera, Echo360 ต้องคิดแบบ responsible engineer

### YouTube

อย่าเริ่ม MVP ด้วยการ download video/audio จาก YouTube อัตโนมัติ เพราะ platform policy มีข้อจำกัดเรื่องการ download/cache audiovisual content

ทำได้ปลอดภัยกว่า:

- ให้ user upload `.vtt` subtitle file เอง
- ให้ user paste transcript ที่เขามีสิทธิ์ใช้
- embed/link YouTube เพื่อดูต้นทาง ไม่ดึง video มาเก็บ
- ในอนาคตใช้ official API เฉพาะกรณีที่ authorization และ policy อนุญาต

### Coursera

อย่า scrape Coursera content เพราะ Terms of Use จำกัด scraping/text/data mining โดยไม่ได้รับอนุญาต

ทำได้ปลอดภัยกว่า:

- ให้ user upload notes, PDF, subtitle ที่ดาวน์โหลดได้อย่างถูกสิทธิ์
- สร้าง “personal study assistant” จากไฟล์ที่ user ให้มา ไม่ใช่ crawler

### Echo360 / EchoVideo

EchoVideo มี API/reporting/caption/transcript concepts สำหรับสถาบัน แต่ access ขึ้นกับ institution permission

ทำได้ปลอดภัยกว่า:

- เริ่มจาก user-uploaded transcript/caption
- ถ้าจะ integrate จริง ต้องใช้ official institution-approved API และ consent

### Australia Privacy

ถ้ารับ lecture files, audio, transcript, user notes อาจมี personal information (ข้อมูลส่วนบุคคล) ได้ ต้องคิดเรื่อง:

- access control
- encryption at rest/in transit
- delete data เมื่อไม่จำเป็น
- ไม่ expose API keys ใน browser
- log เฉพาะ metadata ที่จำเป็น ไม่ log full private lecture โดยไม่จำเป็น

## 4. Recommended Architecture

สำหรับ 1 สัปดาห์และ portfolio: **Modular Monolith (โมดูลาร์โมโนลิธ)** ดีที่สุด

เหตุผล:

- deploy ง่าย
- debug ง่าย
- tests ง่าย
- แต่ยังแยก module boundaries ได้
- ยังไม่ต้องจ่าย complexity ของ microservices

### High-Level Components

- Web App: Next.js หรือ frontend ที่คุณถนัด
- Backend API: FastAPI
- Database: PostgreSQL
- Vector Search: pgvector หรือ vector store managed service
- Object Storage: local ใน dev, S3/Supabase Storage ใน production
- Background Jobs: worker/queue สำหรับ file processing
- AI Provider: LLM, embeddings, speech-to-text, text-to-speech
- Observability: request logs, AI latency, token usage, retrieval traces

### Module Boundaries

- lectures: สร้างและจัดการ lecture workspace
- ingestion: parse files เป็น Canonical Document
- translation: แปล text และดูแล glossary
- summarisation: สร้าง structured notes
- retrieval: chunk, embed, search, cite
- review: quiz, flashcards, concept comparison
- live_translation: future module หลัง MVP

### Data Flow

1. User creates lecture
2. User uploads files
3. Ingestion parses files into segments
4. Segments are normalized into chunks
5. Chunks are embedded and stored
6. Translation and summary are generated from chunks
7. Q&A retrieves relevant chunks before answering
8. Answer includes citations
9. Review module creates quizzes/flashcards from grounded chunks

## 5. Core Domain Model

คิดแบบ domain-driven design (DDD / ออกแบบจากภาษาธุรกิจ)

### Entities

- Lecture: workspace หนึ่งวิชา/หนึ่งบทเรียน
- SourceFile: ไฟล์ต้นทางที่ upload
- Segment: text ที่ parse มา พร้อม metadata เช่น page/slide/timestamp
- Chunk: หน่วยย่อยสำหรับ retrieval
- Translation: translated content ต่อ chunk หรือ section
- Summary: structured lecture note
- Question: user question
- Answer: AI answer พร้อม citations
- ReviewItem: quiz/flashcard/concept comparison
- ProcessingJob: งานเบื้องหลัง เช่น parse/embed/translate
- EvalCase: test case สำหรับคุณภาพ AI

### Invariants (กฎที่ต้องจริงเสมอ)

- Segment ต้องรู้ว่ามาจาก SourceFile ไหน
- Answer ที่อ้าง lecture content ต้องมี citations
- Translation ต้องรู้ target_language
- Chunk ต้องย้อนกลับไปหา source metadata ได้
- Job failure ห้ามทำให้ Lecture หาย
- Private file ต้องไม่ถูกอ่านโดย user คนอื่น

## 6. Design Patterns You Should Explain In Interviews

### Adapter Pattern (ตัวแปลง interface)

ใช้กับ file parser:

- TXTAdapter
- PDFAdapter
- PPTXAdapter
- VTTAdapter
- ImageOCRAdapter ในอนาคต

เหตุผล: แต่ละ file type มี parsing logic ต่างกัน แต่ระบบหลักอยากเรียก `parse(source)` เหมือนกัน

Interview angle:

> ผมใช้ Adapter เพื่อแยก file-format complexity ออกจาก ingestion service ทำให้เพิ่ม DOCX/Image OCR ภายหลังโดยไม่กระทบ workflow หลัก

### Factory Pattern (ตัวเลือก implementation)

ใช้กับการเลือก adapter จาก file extension หรือ MIME type

เหตุผล: service ไม่ควรรู้รายละเอียดว่า `.pdf` ต้องใช้ class ไหนโดยตรง

### Repository Pattern (ชั้นเข้าถึงข้อมูล)

ใช้กับ lecture/source/chunk storage

เหตุผล: domain service ไม่ควรรู้ว่าเก็บใน memory, PostgreSQL, หรือ test fake

### Service Layer (ชั้น business use case)

ใช้กับ create lecture, ingest file, generate summary, answer question

เหตุผล: router/controller ควรบาง และ business logic ควรถูก test ได้โดยไม่ต้องเปิด web server

### Strategy Pattern (เลือกวิธีทำงาน)

ใช้กับ:

- translation strategy: fast vs high-quality
- retrieval strategy: vector-only vs hybrid search
- chunking strategy: by page, by slide, by timestamp, by semantic boundary

### Pipeline Pattern (ลำดับการประมวลผล)

ใช้กับ ingestion:

validate -> save -> parse -> segment -> chunk -> embed -> index

เหตุผล: แต่ละ step test แยกได้ และ retry ได้

### Circuit Breaker / Retry (กัน dependency ล่ม)

ใช้กับ AI provider calls

เหตุผล: model API อาจ timeout/rate limit ต้องไม่ทำให้ app พังทั้งระบบ

### Observer / Tracing (ติดตามระบบ)

ใช้กับ observability:

- AI latency
- token usage
- retrieval chunks
- model name
- failures

เหตุผล: AI app ที่ debug ไม่ได้คือ production risk

## 7. AI System Design

### Translation

อย่าแปลทั้ง lecture ด้วย prompt เดียว

ควรทำ:

- chunk lecture เป็นส่วน ๆ
- extract glossary ก่อน เช่น “attention mechanism”, “gradient descent”
- กำหนด terminology policy
- translate chunk พร้อม context สั้น ๆ
- store translation per chunk
- run consistency checks

Thai output style:

- jargon สำคัญเก็บ English ไว้ แล้วใส่ Thai ในวงเล็บ เช่น `embedding (เวกเตอร์แทนความหมาย)`
- ถ้าศัพท์ไทยไม่ธรรมชาติ ให้ใช้ English
- ไม่แปลชื่อ algorithm/model โดยมั่ว

### Summary

Structured summary ควรมี:

- overview
- key concepts
- definitions
- examples
- formulas/steps ถ้ามี
- common misunderstandings
- review checklist
- citations

### RAG

RAG ไม่ใช่ “ใส่ vector DB แล้วจบ”

ต้องคิด:

- chunk size
- chunk overlap
- metadata
- embedding model
- top-k
- reranking
- citation mapping
- refusal when evidence missing
- eval for answer groundedness

### Lecture Review

Review activities ที่ดี:

- quiz: วัดความเข้าใจ
- flashcards: จำศัพท์และ definition
- concept comparison: เปรียบเทียบ concept ที่สับสนง่าย
- explain like I am beginner: อธิบาย concept ยาก
- exam-style questions: สำหรับเตรียมสอบ

### Live Translation

เก็บไว้หลัง MVP เพราะต้องแก้หลายเรื่องพร้อมกัน:

- microphone/browser permission
- streaming audio
- speech-to-text latency
- translation latency
- text-to-speech latency
- captions sync
- privacy/consent
- fallback เมื่อ network แย่

หลัง MVP ค่อยทำ live translation เป็น 2 mode:

- caption mode: speech-to-text -> translate -> show subtitles
- voice mode: speech-to-text -> translate -> text-to-speech

## 8. 7-Day Plan: 4 Hours Per Day

ใช้สูตรทุกวัน (ปรับจาก 3 ชม. เป็น 4 ชม. ตามที่ผู้เรียนขอ):

- 40 min: design/read/decide (อ่าน source ที่เกี่ยวข้องของวันนั้น + ตัดสินใจ trade-off ก่อนเขียนโค้ด)
- 120 min: build one vertical slice (เขียนโค้ดจริง ทีละ step พร้อม code review แทรกระหว่างทาง)
- 60 min: test/eval (unit test, manual API test ผ่าน /docs, eval case ถ้ามี AI component)
- 20 min: write notes + screenshot evidence + ซ้อมตอบ interview question ของวันนั้น 2-3 ข้อ

### Day 1 - Product, Repo, Architecture

Outcome:

- repo ของคุณเอง
- PRD
- architecture doc
- ADR: modular monolith
- first health endpoint or skeleton app

ต้องเข้าใจ:

- problem vs solution
- MVP slicing
- modular monolith
- user journey
- source/legal boundary

Build:

- create repo from scratch
- write README with product story
- create `docs/PRD.md`
- create `docs/ARCHITECTURE.md`
- create `docs/adr/001-modular-monolith.md`
- setup backend skeleton

Screenshot ที่ต้องเก็บ:

- repo structure
- first API docs/health page
- PRD/architecture docs

Interview questions:

- Why not microservices?
- What is the smallest useful MVP?
- How would you avoid scraping protected lecture platforms?
- What makes this more than a translation wrapper?

### Day 2 - Lecture And Ingestion Domain

Outcome:

- create lecture
- parse TXT/VTT
- parse PDF/PPTX if time allows
- canonical document model
- tests for parser

ต้องเข้าใจ:

- domain entity
- adapter pattern
- factory pattern
- metadata preservation

Build:

- Lecture entity
- SourceFile entity
- Segment entity
- TXTAdapter
- VTTAdapter
- route/service for parse file
- tests with sample files

Screenshot ที่ต้องเก็บ:

- passing tests
- API response showing segments
- VTT timestamp parsed correctly

Interview questions:

- How do you preserve citations from heterogeneous files?
- Why is Canonical Document useful?
- How would you add image OCR without rewriting ingestion?

### Day 3 - Chunking, Citations, Storage Design

Outcome:

- chunking design
- source citation model
- database schema draft
- metadata strategy

ต้องเข้าใจ:

- chunking strategy
- citation traceability
- relational model vs vector model
- background processing

Build:

- Chunk domain model
- citation object
- chunking service
- storage interface
- first database migration if ready

Quality checks:

- every chunk maps back to file/page/slide/timestamp
- chunks are not too big for prompt context
- empty files handled cleanly

Screenshot ที่ต้องเก็บ:

- chunks with citations
- test proving citation survives parsing/chunking

Interview questions:

- What chunk size would you start with and why?
- How do you prevent generated answers without evidence?
- What metadata must be stored for trustworthy RAG?

### Day 4 - Translation And Summary

Outcome:

- translation workflow design
- glossary policy
- summary format
- first AI integration behind an interface

ต้องเข้าใจ:

- prompt contract
- terminology consistency
- model abstraction
- eval-driven development

Build:

- TranslationService interface
- SummaryService interface
- glossary extraction plan
- prompt files or prompt templates
- fake model for tests

Quality checks:

- Thai output keeps jargon as English(Thai)
- Mandarin/Thai target language validated
- summary includes citations or source references

Screenshot ที่ต้องเก็บ:

- translated sample
- summary sample
- eval table for terminology consistency

Interview questions:

- How do you evaluate translation quality?
- How do you control cost for long lectures?
- Why use fake model in tests?

### Day 5 - RAG Q&A And Lecture Review

Outcome:

- ask question about lecture
- retrieve relevant chunks
- answer with citations
- generate review items

ต้องเข้าใจ:

- embeddings
- vector search
- hybrid search
- grounded answer
- review generation

Build:

- RetrievalService
- AnswerService
- ReviewService
- vector storage decision
- eval cases for Q&A

Quality checks:

- answer refuses when no evidence
- citation points to correct source
- quiz answer key is grounded

Screenshot ที่ต้องเก็บ:

- Q&A answer with citations
- failed/no-evidence case
- flashcards/quiz result

Interview questions:

- What is RAG and when does it fail?
- How would you debug bad retrieval?
- Why might hybrid search be better than vector search only?

### Day 6 - Frontend UX And End-To-End Flow

Outcome:

- usable web flow
- upload multiple files
- show processing status
- show summary/translation/Q&A/review

ต้องเข้าใจ:

- UX for async jobs
- loading/error/empty states
- accessibility basics
- API contract

Build:

- lecture create screen
- upload screen
- file list/status
- summary tab
- Q&A tab
- review tab

Quality checks:

- user can finish journey without reading docs
- long text does not overflow
- error messages are understandable

Screenshot ที่ต้องเก็บ:

- create lecture screen
- multi-upload screen
- summary tab
- Q&A with citation
- mobile viewport

Interview questions:

- How do you design UX for long-running AI tasks?
- What happens if one uploaded file fails?
- How do you communicate AI uncertainty to users?

### Day 7 - Deployment, Observability, Demo Story

Outcome:

- deployed demo
- README polished
- architecture diagram
- eval results
- demo script
- resume/interview story

ต้องเข้าใจ:

- environment variables
- secrets
- CI/test command
- production logging
- privacy basics
- cost controls

Build:

- production config
- deploy frontend/backend
- health check
- seed sample lecture
- demo script
- README screenshots

Quality checks:

- app deploys from clean checkout
- secrets are not committed
- health endpoint works
- key user journey works

Screenshot ที่ต้องเก็บ:

- deployed URL
- health endpoint
- README
- final demo flow
- test pass

Interview questions:

- How would you monitor this in production?
- What logs would you keep and what would you avoid logging?
- What would you do if AI cost spikes?
- How would you scale from 10 users to 10,000 users?

## 9. Starting Your Own Repo

Do not clone a tutorial repo.

Start with this order:

1. Write one paragraph problem statement.
2. Write 5 user stories.
3. Write out-of-scope list.
4. Create architecture doc.
5. Create first ADR.
6. Create backend skeleton.
7. Add one vertical slice end-to-end.
8. Add tests.
9. Add UI.
10. Deploy.

Repo structure suggestion:

- `apps/web` - frontend
- `apps/api` - backend
- `docs` - PRD, architecture, ADRs, interview notes
- `samples` - sample files safe to commit
- `evals` - evaluation cases and expected behavior

README sections:

- problem
- demo screenshots
- architecture
- features
- what I intentionally did not build
- local setup
- testing
- deployment
- lessons learned

## 10. What To Say In Interviews

### Project Pitch

> I built LectureBridge AI, an AI learning assistant for international students. It ingests lecture PDFs, slides, text, and subtitle files, preserves source metadata, translates content into Thai or Mandarin, generates structured notes, and answers questions using RAG with citations. I started with uploaded files instead of live video because I wanted the MVP to be privacy-aware, legally safer, testable, and citation-grounded before adding low-latency audio streaming.

### Strong Technical Story

> The core design decision was to create a Canonical Document model. Every parser returns segments with metadata, so the rest of the system does not care if the source was a PDF page, PPT slide, or VTT timestamp. This made translation, summarization, RAG, and review generation all reuse the same pipeline.

### Strong AI Story

> I treated AI outputs as probabilistic, so I added eval cases instead of relying on manual vibe checks. I measured whether answers were grounded in retrieved chunks, whether citations were present, and whether key terminology stayed consistent across translations.

### Strong FDE Story

> The user did not ask for a chatbot. The actual problem was lecture comprehension under language pressure. So I designed the product around the student workflow: collect materials, understand concepts, ask questions, review before exams, and verify source evidence.

## 11. Real Case Interview Questions

### System Design

1. Design a system that translates university lectures into Thai/Mandarin and supports Q&A with citations.
2. How would you support PDF, PPTX, VTT, and images without making the ingestion service messy?
3. How would you process a 2-hour lecture transcript without sending the whole transcript to the LLM every time?
4. How would you design the database schema for source traceability?
5. How would you add live translation after the document MVP?

### AI Engineering

1. What is the difference between summarization and RAG?
2. How do embeddings work at a product level?
3. What causes hallucination in a RAG system?
4. How would you evaluate translation quality for academic terms?
5. How would you choose between vector search and hybrid search?
6. How do you reduce LLM cost without hurting quality too much?
7. What would you log for AI observability?

### Backend Engineering

1. Why use background jobs for file processing?
2. What happens if PDF parsing succeeds but embedding fails?
3. How would you design retry behavior for external AI APIs?
4. How would you secure uploaded lecture files?
5. How would you make tests deterministic when AI output is nondeterministic?

### Product/FDE

1. A university asks for Echo360 integration. What questions do you ask first?
2. A student says the translation is wrong for technical terms. How do you diagnose?
3. The system gives a correct answer but bad citation. Is that acceptable?
4. Coursera content is behind login. How do you handle it responsibly?
5. A customer wants live voice translation next week. What MVP do you propose?

### Australia/Sydney Career

1. How would you explain the difference between AI Engineer, Data Scientist, and Software Engineer?
2. How do you build production-grade GenAI instead of a demo?
3. What governance/privacy concerns matter for an Australian user-upload app?
4. How would you present this project to a bank, university, or government team?

## 12. Common Mistakes To Avoid

- building live translation first
- relying on one giant prompt
- no citations
- no evals
- no tests around parser/chunking
- no failure states in UI
- storing API keys in frontend
- committing private lecture files
- calling everything an agent
- building microservices before product-market learning
- copying tutorial repo structure without understanding trade-offs

## 13. Source Notes

Provided sources to study:

- YouTube live: https://www.youtube.com/live/bjkjaqUZl4E
- Krish Naik Agentic AI course link: https://www.youtube.com/watch?v=rV3HJ4LEZ7k
- Krish Naik GitHub: https://github.com/krishnaik06
- FDE project video: https://www.youtube.com/watch?v=FSZhPDzESPU
- pgvector tutorial video: https://www.youtube.com/watch?v=Ff3tJ4pJEa4
- Additional videos: https://www.youtube.com/watch?v=1a1VXDdIyrk and https://www.youtube.com/watch?v=TbtBhbLh0cc

High-trust references:

- ABS AI Engineer occupation draft: https://www.abs.gov.au/statistics/classifications/consultation-draft-occupation-standard-classification-australia-osca/aug-2026/browse-classification/2/27/273/2733/273334
- Jobs and Skills Australia Software Engineer profile: https://www.jobsandskills.gov.au/data/occupation-and-industry-profiles/occupations-osca/273333-software-engineer
- ACS Digital Pulse: https://www.acs.org.au/campaign/digital-pulse.html
- OpenAI API docs: https://developers.openai.com/api/
- OpenAI speech-to-text docs: https://developers.openai.com/api/docs/guides/speech-to-text
- OpenAI Realtime docs: https://developers.openai.com/api/docs/guides/realtime
- OpenAI evaluation best practices: https://developers.openai.com/api/docs/guides/evaluation-best-practices
- FastAPI docs: https://fastapi.tiangolo.com/
- Next.js App Router docs: https://nextjs.org/docs/app
- pgvector README: https://github.com/pgvector/pgvector
- YouTube API developer policies: https://developers.google.com/youtube/terms/developer-policies
- YouTube captions API docs: https://developers.google.com/youtube/v3/docs/captions/list
- Coursera Terms of Use: https://www.coursera.org/about/terms
- EchoVideo API/support docs: https://support.echo360.com/hc/en-us/sections/10967188719245-API
- OAIC Australian Privacy Principles: https://www.oaic.gov.au/privacy/australian-privacy-principles/read-the-australian-privacy-principles

