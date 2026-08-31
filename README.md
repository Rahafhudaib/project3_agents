# Project 3 - Multi-Agent RAG System

نظام محادثة مع المستندات (PDF / DOCX / TXT) باستخدام ثلاثة Agents متعاونين:
Retriever Agent, Analyst Agent, Answer Agent، بالإضافة إلى Document Pipeline
لتجهيز الملفات و Vector DB لتخزينها.

## فكرة النظام

1. **Document Pipeline**: يقرأ الملفات من مجلد `data/`، ينظف النص، يقسمه إلى
   Chunks، يحول كل Chunk إلى Embedding، ويخزنها في Vector DB محلي (ملف
   pickle).
2. **Retriever Agent**: يعيد صياغة السؤال، يبحث Semantic + Keyword (BM25)،
   يفلتر حسب الميتاداتا، يعمل Rerank، ثم يختار أفضل مجموعة Chunks.
3. **Analyst Agent**: يحلل الأدلة، يستخرج الأرقام والجداول، يقارن بين
   المستندات، ويقرر إذا كانت الأدلة كافية. إذا لم تكن كافية يرجع للـ
   Retriever Agent (Feedback Loop).
4. **Answer Agent**: يبني الإجابة النهائية مع الاستشهادات (اسم الملف ورقم
   الصفحة).

الـ Orchestrator في `agents/orchestrator.py` هو من يربط الثلاثة Agents مع
بعض.

## المتطلبات

- Python 3.10 أو أحدث
- مفتاح OpenAI API (يستخدم للـ Query Rewriting و التحليل وتوليد الإجابة)

## التثبيت

```bash
cd project3_rag
python -m venv venv
source venv/bin/activate    # على ويندوز: venv\Scripts\activate
pip install -r requirements.txt
```

ثم فعّل مفتاح الـ API:

```bash
export OPENAI_API_KEY="sk-..."      # على ويندوز: set OPENAI_API_KEY=sk-...
```

## طريقة الاستخدام

1. حط ملفات الـ PDF / DOCX / TXT اللي بدك تسأل عنها داخل مجلد `data/`.
2. شغل البرنامج:

```bash
python main.py
```

3. أول مرة رح يفهرس (Index) الملفات تلقائياً، وبعدها تقدر تسأل مباشرة من
   الـ Terminal.
4. لو ضفت ملفات جديدة، اكتب `reindex` عشان يعيد الفهرسة.
5. لإنهاء البرنامج اكتب `exit`.

## هيكل المشروع

```
project3_rag/
├── main.py
├── config.py
├── llm.py
├── requirements.txt
├── data/                      # حط ملفاتك هون
├── document_pipeline/
│   ├── loader.py              # قراءة PDF / DOCX / TXT
│   ├── cleaner.py             # تنظيف النص
│   ├── chunker.py             # تقسيم النص لأجزاء
│   ├── embeddings.py          # تحويل النص لمتجهات
│   ├── vector_db.py           # قاعدة بيانات المتجهات (محلية)
│   └── ingest.py              # يربط كل خطوات التجهيز مع بعض
├── agents/
│   ├── retriever_agent.py
│   ├── analyst_agent.py
│   ├── answer_agent.py
│   └── orchestrator.py
└── tools/
    ├── calculator.py
    ├── table_extractor.py
    ├── document_comparison.py
    └── data_analysis.py
```

## ملاحظات

- كل شي يشتغل Local، ما في أي Deployment أو Server خارجي، غير نداء الـ
  OpenAI API للتحليل وتوليد الإجابة.
- الـ Embeddings تستخدم مكتبة `sentence-transformers` وتشتغل محلياً على
  جهازك (بيحمل الموديل أول مرة بس).
- ملف `vector_store.pkl` هو قاعدة البيانات المحلية، احذفه إذا بدك تبدأ من
  الصفر.
