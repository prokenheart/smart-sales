import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from "@mui/material";
import type { Dispatch, SetStateAction } from "react";

export default function ConfirmDelete({
  openConfirm,
  setOpenConfirm,
  setConfirmDelete,
  setDeleteId,
}: Readonly<{
  openConfirm: boolean;
  setOpenConfirm: Dispatch<SetStateAction<boolean>>;
  setConfirmDelete: Dispatch<SetStateAction<boolean>>;
  setDeleteId: Dispatch<SetStateAction<string | undefined>>;
}>) {
  return (
    <Dialog
      open={openConfirm}
      hideBackdrop
      onClose={(_, reason) => {
        if (reason === "escapeKeyDown" || reason === "backdropClick") return;
      }}
    >
      <DialogTitle>Confirm Delete</DialogTitle>
      <DialogContent>Are you sure to delete this</DialogContent>
      <DialogActions>
        <Button
          onClick={() => {
            setOpenConfirm(false);
            setDeleteId(undefined);
          }}
        >
          No
        </Button>
        <Button
          onClick={() => {
            setConfirmDelete(true);
          }}
        >
          Yes
        </Button>
      </DialogActions>
    </Dialog>
  );
}
