import { Dialog, DialogContent } from "@mui/material";
import type { ReactElement, Dispatch, SetStateAction } from "react";

const AttachmentPreviewDialog = ({
  viewURL,
  isOpen,
  setIsOpen,
  setViewURL,
}: Readonly<{
  viewURL: string | null;
  isOpen: boolean;
  setIsOpen: Dispatch<SetStateAction<boolean>>;
  setViewURL: Dispatch<SetStateAction<string | null>>;
}>): ReactElement => {
  const handleClose = (): void => {
    setIsOpen(false);
    setViewURL(null);
  };

  const isPdf = viewURL
    ? new URL(viewURL).pathname.toLowerCase().endsWith(".pdf")
    : false;

  return (
    <Dialog open={isOpen} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogContent>
        {viewURL &&
          (isPdf ? (
            <iframe
              src={viewURL}
              title="PDF Preview"
              style={{
                width: "100%",
                height: "500px",
                border: "none",
              }}
            />
          ) : (
            <img
              src={viewURL}
              alt="Preview"
              style={{
                width: "100%",
                height: "400px",
                objectFit: "contain",
              }}
            />
          ))}
      </DialogContent>
    </Dialog>
  );
};

export default AttachmentPreviewDialog;
