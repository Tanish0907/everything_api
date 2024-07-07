import axios from "axios";
import "./index.css";
import { Modal } from "react-bootstrap";
import { createRoot } from "react-dom/client";
import { useState } from "react";
import { Comic_Info } from "../Comic_info";

export const Comic_card = (props) => {
  const [dialog, setDialog] = useState(false);
  return (
    <>
      <div
        className="comic_card_body"
        onClick={() => {
          setDialog(true);
        }}
        style={{
          backgroundImage: `url(${props.img})`,
          backgroundRepeat: "no-repeat",
          backgroundSize: "contain",
          backgroundPosition: "center",
        }}
      >
        <div className="name">{props.name}</div>
      </div>
      <Modal
        size="xl"
        id="dialog_box"
        show={dialog}
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
          <div id="comic_info">
              <Comic_Info id={props.id} poster={props.img} />
          </div>
        </Modal.Body>
      </Modal>
    </>
  );
};
