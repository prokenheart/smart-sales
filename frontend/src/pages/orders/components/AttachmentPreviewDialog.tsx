import { Dialog, DialogContent } from "@mui/material";
import type { ReactElement, Dispatch, SetStateAction } from "react";

const AttachmentPreviewDialog = ({
  viewURL,
  open,
  setOpen,
  setViewURL,
}: Readonly<{
  viewURL: string | null;
  open: boolean;
  setOpen: Dispatch<SetStateAction<boolean>>;
  setViewURL: Dispatch<SetStateAction<string | null>>;
}>): ReactElement => {
  const handleClose = (): void => {
    setOpen(false);
    setViewURL(null);
  };

  return (
    <Dialog open={open} onClose={handleClose}>
      <DialogContent>
        <img
          src={viewURL ?? ""}
          alt="Preview"
          style={{
            width: "100%",
            height: "400px",
            objectFit: "contain",
          }}
        />
      </DialogContent>
    </Dialog>
  );
};

export default AttachmentPreviewDialog;
