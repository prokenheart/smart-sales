import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from "@mui/material";
import type { Dispatch, SetStateAction } from "react";

export default function ConfirmClose({
  openConfirm,
  setOpenConfirm,
  setConfirmClose,
}: Readonly<{
  openConfirm: boolean;
  setOpenConfirm: Dispatch<SetStateAction<boolean>>;
  setConfirmClose: Dispatch<SetStateAction<boolean>>;
}>) {
  return (
    <Dialog
      open={openConfirm}
      hideBackdrop
      onClose={(_, reason) => {
        if (reason === "escapeKeyDown" || reason === "backdropClick") return;
      }}
    >
      <DialogTitle>Confirm Exit</DialogTitle>
      <DialogContent>Are you sure to exit without saving</DialogContent>
      <DialogActions>
        <Button
          onClick={() => {
            setOpenConfirm(false);
          }}
        >
          No, I'll stay
        </Button>
        <Button
          onClick={() => {
            setConfirmClose(true);
          }}
        >
          Yes
        </Button>
      </DialogActions>
    </Dialog>
  );
}
