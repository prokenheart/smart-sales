import type { ReactElement, Dispatch, SetStateAction } from "react";
import { createViewAttachmentURL } from "@services/order";
import { Button } from "@mui/material";

const AttachmentPreviewButton = ({
  orderId,
  setViewURL,
  setIsOpenViewDialog,
}: Readonly<{
  orderId: string;
  setViewURL: Dispatch<SetStateAction<string | null>>;
  setIsOpenViewDialog: Dispatch<SetStateAction<boolean>>;
}>): ReactElement => {
  const createUrl = async () => {
    const res = await createViewAttachmentURL(orderId);
    setViewURL(res.data.getUrl);
  };

  return (
    <Button
      onClick={(e) => {
        e.stopPropagation();
        createUrl();
        setIsOpenViewDialog(true);
      }}
      variant="outlined"
      sx={{
        color: "secondary.contrastText",
        borderColor: "secondary.contrastText",
        backgroundColor: "primary.contrastText",
        "&:hover": {
          color: "primary.main",
        },
      }}
    >
      View File
    </Button>
  );
};

export default AttachmentPreviewButton;
