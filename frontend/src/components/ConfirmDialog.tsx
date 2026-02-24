import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Typography,
} from "@mui/material";
import type { ReactElement } from "react";

type ConfirmDialogProps = {
  open: boolean;
  title: string;
  description: string;
  onConfirm: () => void;
  onCancel: () => void;
};

const ConfirmDialog = ({
  open,
  title,
  description,
  onConfirm,
  onCancel,
}: Readonly<ConfirmDialogProps>): ReactElement => {
  return (
    <Dialog
      open={open}
      onClose={(_, reason) => {
        if (reason === "escapeKeyDown" || reason === "backdropClick") return;
        onCancel();
      }}
    >
      <DialogTitle>
        <Typography variant="h6">{title}</Typography>
      </DialogTitle>
      <DialogContent>
        <Typography variant="body2">{description}</Typography>
      </DialogContent>

      <DialogActions>
        <Button onClick={onCancel}>No</Button>
        <Button onClick={onConfirm} color="warning">
          Yes
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ConfirmDialog;
