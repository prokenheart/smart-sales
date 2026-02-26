import { type ReactElement, useState } from "react";
import { Dialog, Box, Button, Stack } from "@mui/material";
import ConfirmDialog from "../../../components/ConfirmDialog";

const FilePreviewDialog = ({
  open,
  preview,
  onCancel,
  onConfirm,
}: Readonly<{
  open: boolean;
  preview: string | undefined;
  onCancel: () => void;
  onConfirm: () => void;
}>): ReactElement => {
  const [openConfirm, setOpenConfirm] = useState<boolean>(false);

  return (
    <Dialog
      open={open}
      onClose={() => {
        setOpenConfirm(true);
      }}
      maxWidth="md"
      fullWidth
    >
      <Box mt={2}>
        <img
          src={preview}
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
        sx={{
          pr: 2,
          pb: 2,
        }}
      >
        <Button onClick={onCancel} variant="outlined" color="error">
          Cancel
        </Button>

        <Button onClick={onConfirm} variant="contained">
          Upload
        </Button>
      </Stack>
      <ConfirmDialog
        open={openConfirm}
        title="Confirm Close"
        description="Are you sure to exit without saving"
        onCancel={() => {
          setOpenConfirm(false);
        }}
        onConfirm={() => {
          setOpenConfirm(false);
          onCancel();
        }}
      />
    </Dialog>
  );
};

export default FilePreviewDialog;
