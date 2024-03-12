## Setup
1- Create .env file where you store ASTRA_DB_APPLICATION_TOKEN, OPENAI_API_KEY and ASTRA_DB_ID <br />
2- Create a database using dataStax. You can follow the steps in the following doc: https://docs.datastax.com/en/astra-classic/docs/manage/db/manage-create.html <br />

## Run:
Build your docker image then run it
```bash
docker build -t image_name .
```
```bash
docker run -p 8000:8000 image_name
```
Use this url to test the API: http://localhost:8000/docs
You'll find two section: 
![Screenshot 2024-03-12 191930](https://github.com/bbelkis/simple-chatbot-with-openai-and-Langchain/assets/161017991/1fa47034-baf2-40f1-b981-e28d6df5e7fc)
In the first section you can upload your pdf: 
![Screenshot 2024-03-12 192005](https://github.com/bbelkis/simple-chatbot-with-openai-and-Langchain/assets/161017991/822c9935-b112-4b4a-978a-26cf899d09fa)
In the second section you can query it:
![Screenshot 2024-03-12 192033](https://github.com/bbelkis/simple-chatbot-with-openai-and-Langchain/assets/161017991/42a5d7b0-8aed-48d7-8fd7-9d7dc2df013c)
