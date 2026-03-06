import { type ReactElement, useState } from "react";
import { Dialog, Box, Button, Stack } from "@mui/material";
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
  onConfirm: () => void;
}>): ReactElement => {
  const [isOpenConfirm, setIsOpenConfirm] = useState(false);

  return (
    <Dialog
      open={isOpen}
      onClose={() => {
        setIsOpenConfirm(true);
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

        <Button onClick={onConfirm} variant="contained">
          Upload
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
