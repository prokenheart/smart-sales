import { type ReactElement, useState } from "react";
import { Dialog, Box, Button, Stack, CircularProgress } from "@mui/material";
import ConfirmDialog from "@components/ConfirmDialog";

const FilePreviewDialog = ({
  isOpen,
  previewPickedFileSrc,
  onCancel,
  onConfirm,
}: Readonly<{
  isOpen: boolean;
  previewPickedFileSrc: string;
  onCancel: () => void;
  onConfirm: () => Promise<void>;
}>): ReactElement => {
  const [isOpenConfirm, setIsOpenConfirm] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const handleUpload = async () => {
    try {
      setIsUploading(true);
      await onConfirm();
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Dialog
      open={isOpen}
      onClose={() => {
        if (!isUploading) setIsOpenConfirm(true);
      }}
      maxWidth="md"
      fullWidth
    >
      <Box mt={2}>
        <img
          src={previewPickedFileSrc}
          alt="preview"
          style={{
            width: "100%",
            height: "400px",
            objectFit: "contain",
          }}
        />
      </Box>
      <Stack
        direction={"row"}
        justifyContent={"flex-end"}
        spacing={2}
        pr={2}
        pb={2}
      >
        <Button onClick={onCancel} variant="outlined" color="error">
          Cancel
        </Button>

        <Button
          onClick={handleUpload}
          variant="contained"
          disabled={isUploading}
        >
          {isUploading ? <CircularProgress size={20} /> : "Upload"}
        </Button>
      </Stack>
      <ConfirmDialog
        isOpen={isOpenConfirm}
        title="Confirm Close"
        description="Are you sure to exit without saving"
        onCancel={() => {
          setIsOpenConfirm(false);
        }}
        onConfirm={() => {
          setIsOpenConfirm(false);
          onCancel();
        }}
      />
    </Dialog>
  );
};

export default FilePreviewDialog;
