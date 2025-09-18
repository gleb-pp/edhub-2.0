"use client";

import { Button } from "@/shared/ui/button/button";
import { Modal } from "@/shared/ui/modal/modal";
import { useState } from "react";

export default function Home() {
  const [isOpen, setOpen] = useState(false);

  function handleOpenModal() {
    setOpen(true);
  }

  function handleCloseModal() {
    setOpen(false);
  }

  return (
    <div className="p-10">
      <Button onClick={handleOpenModal} className="px-6 py-1 rounded-md">
        Open Modal
      </Button>
      <Modal
        className="p-5 w-200 h-80"
        isOpen={isOpen}
        onClose={handleCloseModal}
      >
        <Modal.Header>Modal header</Modal.Header>
        <Modal.Body>Modal body</Modal.Body>
        <Modal.Footer>Modal footer</Modal.Footer>
      </Modal>
    </div>
  );
}
