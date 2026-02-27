import { Dialog, DialogContent } from "@mui/material";
import type { ReactElement, Dispatch, SetStateAction } from "react";

const AttachmentPreviewDialog = ({
  viewURL,
  open,
  setOpen,
  setViewURL,
}: Readonly<{
  viewURL: string | undefined;
  open: boolean;
  setOpen: Dispatch<SetStateAction<boolean>>;
  setViewURL: Dispatch<SetStateAction<string | undefined>>;
}>): ReactElement => {
  const handleClose = (): void => {
    setOpen(false);
    setViewURL(undefined);
  };

  return (
    <Dialog open={open} onClose={handleClose}>
      <DialogContent>
        <img
          src={viewURL}
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
