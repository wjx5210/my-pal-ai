import axios from "axios";
import ReactMarkdown from "react-markdown";
import PalCard from "./PalCard";


type Source = {
  name:string;
  type:string;
  url:string;
};


type Props = {

 question:string;

 setQuestion:(value:string)=>void;

 answer:string;

 setAnswer:(value:string)=>void;

 sources:Source[];

 setSources:(value:Source[])=>void;

 loading:boolean;

 setLoading:(value:boolean)=>void;

};


function ChatBox({

 question,
 setQuestion,

 answer,
 setAnswer,

 sources,
 setSources,

 loading,
 setLoading

}:Props){

  async function handleSubmit(){

    setLoading(true);

    setAnswer("");
    setSources([]);

    const response = await axios.post(
      "http://127.0.0.1:8000/ask",
      {
        question: question
      }
    );


    setAnswer(response.data.answer);

    setSources(response.data.sources);

    setLoading(false);

  }


  return (
    <div>


      <input
        type="text"
        placeholder="请输入你的问题"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />


      <button onClick={handleSubmit}>
        发送
      </button>


    {
      loading ? (
        <p>
          AI正在思考，请稍候...
        </p>
      ) : answer ? (
        <div>

          <h3>
            AI回答：
          </h3>

          <div className="answer">

            <ReactMarkdown>
                {answer}
            </ReactMarkdown>

          </div>

        </div>
      ) : null
    }
    {
        !loading && sources.length > 0 &&(
            <div>
                <h3>
                    参考帕鲁：
                </h3>

                {
                  sources.map((source)=>(
                    <PalCard
                      key={source.name}
                      name={source.name}
                    />
                  ))
                }

            </div>
                )
    }
    </div>
  )
}


export default ChatBox;