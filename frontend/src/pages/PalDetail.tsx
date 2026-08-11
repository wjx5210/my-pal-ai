import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";


type Pal = {

  name:string;

  element:string[];

  summary:string;

  work_suitability:{
    [key:string]:number;
  };

  drops:string[];

};


function PalDetail(){

  const {name} = useParams();


  const [pal,setPal] = useState<Pal | null>(null);


  useEffect(()=>{


    if(!name){
      return;
    }


    axios
      .get(
        `http://127.0.0.1:8000/pal/${name}`
      )
      .then(res=>{

        setPal(res.data);

      });


  },[name]);



  if(!pal){

    return (
      <div>
        加载中...
      </div>
    )

  }



  return (

    <div>

      <h1>
        {pal.name}
      </h1>


      <h3>
        属性
      </h3>

      <p>
        {pal.element.join("、")}
      </p>


      <h3>
        简介
      </h3>

      <p>
        {pal.summary}
      </p>


      <h3>
        工作能力
      </h3>

      {
        Object.entries(
          pal.work_suitability
        ).map(([key,value])=>(

          <p key={key}>
            {key} Lv.{value}
          </p>

        ))
      }


      <h3>
        掉落
      </h3>

      <p>
        {pal.drops.join("、")}
      </p>


    </div>

  )

}


export default PalDetail;