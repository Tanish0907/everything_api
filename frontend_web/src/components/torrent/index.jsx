import { useState } from "react";
import { Modal } from "react-bootstrap";
import "./index.css"
export const Torr=(props)=>{
  const[Dialog,setDialog]=useState(false);
  return(
    <>
    <div className="card_body" onClick={()=>{setDialog(true)}}>
      <h3>{props.title}</h3>
      <div className="info">
        <p>catagory:{props.cat}</p>
        <p>size:{props.size}</p>
        <p>source:{props.source}</p>
      </div>
    </div>
    <Modal
      size="lg"
      id="dialog_box"
      show={Dialog}
      onHide={() => setDialog(false)}
      dialogClassName="modal-90w"
      aria-labelledby="example-custom-modal-styling-title"
    >
      <Modal.Header closeButton>
        <Modal.Title id="example-custom-modal-styling-title">
          {props.name}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div id="magnet_db">
          
          <div className="mag">{props.mag}</div>
          <a href={props.link}>DOWNLOAD FILE</a>
        </div>
      </Modal.Body>
    </Modal>
    </>
  );
}
