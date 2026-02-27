import type { ReactElement, Dispatch, SetStateAction } from "react";
import { createViewAttachmentURL } from "../../../services/order";
import { Button } from "@mui/material";

const AttachmentPreviewButton = ({
  orderId,
  setViewURL,
  setOpenViewDialog,
}: Readonly<{
  orderId: string;
  setViewURL: Dispatch<SetStateAction<string | undefined>>;
  setOpenViewDialog: Dispatch<SetStateAction<boolean>>;
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
        setOpenViewDialog(true);
      }}
    >
      View File
    </Button>
  );
};

export default AttachmentPreviewButton;
