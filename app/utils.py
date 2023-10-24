from pydantic import BaseModel
import pandas as pd

from langchain.schema import Document
from langchain.llms import LlamaCpp
from langchain.chains import LLMChain, RetrievalQA
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, PromptTemplate
from langchain.document_loaders.pdf import UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS


class MessageInfo(BaseModel):
    message: str
    user_id: str


class Loader:
    def __init__(self, path):
        self.data = []
        self.path = path

    def splitter(self, ol):
        return CharacterTextSplitter(
            separator='\n',
            chunk_size=1024,
            chunk_overlap=ol,
            length_function=len,
        ).transform_documents(self.doc_parsed)

    def process_data(self):
        data_csv = pd.read_csv(self.path + '/cards.csv')
        for i, item in data_csv.iterrows():
            content = f"Сервис: {item['Service']}, Условие: {item['Condition']}, Тариф: {item['Tariff']}"
            self.data.append(Document(page_content=content, metadata={'source': 'tinkoff-terms/cards.csv'}))

        pdf_path = [self.path + '/doc1.pdf', self.path + '/doc2.pdf']
        mas = [1024, 0]

        for doc_loader in [UnstructuredPDFLoader(path) for path in pdf_path]:
            self.doc_parsed = doc_loader.load()

            for ol in mas:
                self.data += self.splitter(ol)

    def get_data(self):
        return self.data


embeddings = HuggingFaceEmbeddings(model_name="cointegrated/rubert-tiny2",
                                   model_kwargs={'device': 'cpu'})


load_data = Loader("app/tinkoff-terms")
load_data.process_data()
db = FAISS.from_documents(load_data.get_data(), embeddings)


def get_promt():
    return PromptTemplate(
        template=(
            "Ты - ассистент банка Тинькофф. Твоя задача ответить на вопрос пользователя, используя информацию из документов.\n"
            "Отвечай честно. Если не знаешь ответ - не придумывай. \n"
            "Не используй нецензурные выражения, отвечай только на русском языке. Ответ должен быть коротким.\n\n"
            "Контекст:\n{context}\n"
            "Вопрос: {question}\n"
            "Ответ:"
        ),
        input_variables=['context', 'question']
    )

def get_llm():
    return LlamaCpp(
        model_path="app/llama-2-7b-chat.Q4_K_M.gguf",
        temperature=0.0,
        max_tokens=2000,
        n_ctx=2000,
        top_p=0.99,
        n_batch=1,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        verbose=True,
)


def get_answer_from_llm(message_info: MessageInfo) -> str:
    qa_with_sources_chain = RetrievalQA.from_chain_type(
        llm=get_llm(),
        retriever=db.as_retriever(search_kwargs={'k': 5}),
        callbacks=[StreamingStdOutCallbackHandler()],
        return_source_documents=True,
        chain_type_kwargs={"prompt": get_promt()}
    )
    answer = qa_with_sources_chain({'query': message_info.message})
    return answer['result']
