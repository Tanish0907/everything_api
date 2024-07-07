import axios from "axios";
import { createRoot } from "react-dom/client";
import "./index.css";
import { Button } from "react-bootstrap";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import { useState,useEffect,useCallback } from "react";
export const Manga_Info = (props) => {
  
  const [Img_lst,setImg_lst]=useState([]);
  const update_root=()=>{
    const root=createRoot(document.getElementById("manga_info")); 
    root.render(
      Img_lst,document.getElementsByClassName("manga_data")
    );
  }
  const fetch_manga=useCallback(async ()=>{
    setImg_lst([]);
    axios
    .get(`http://localhost:8000/manga/${props.id}`)
    .then((res) => {
      const book_pglst=Object.values(res.data);
      const links=book_pglst.reduce((accumulator, value) => accumulator.concat(value), []);
      Img_lst.push(<img className="poster" src={props.poster}/>);
      for(let i=0;i<links.length;i++){
        Img_lst.push(<img className="poster" src={links[i]}/>);
      }
      update_root();
    }).catch((err) => {
      console.log(err);
    });
  },[props.id]);

  useEffect(()=>{
    fetch_manga();
  },[fetch_manga])


  return( 
    <div className="manga_info">
      <div className="manga_data">

          
      </div>
    </div>)
};
