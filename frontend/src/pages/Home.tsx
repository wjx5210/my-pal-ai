import ChatBox from "../components/ChatBox";


function Home(props:any){

  return (
    <div>

      <h1>
        我的帕鲁 AI攻略助手
      </h1>


      <ChatBox
        {...props}
      />


    </div>
  )

}

export default Home;