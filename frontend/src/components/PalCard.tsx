import { Link } from "react-router-dom";


type Props = {
  name: string;
};


function PalCard({name}: Props){

  return (

    <Link
      to={`/pal/${name}`}
      className="pal-link"
    >

      <div className="pal-card">

        <h4>
          {name}
        </h4>

        <p>
          查看帕鲁详情 →
        </p>

      </div>

    </Link>

  )

}


export default PalCard;