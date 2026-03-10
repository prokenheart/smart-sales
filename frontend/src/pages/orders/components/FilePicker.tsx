import { Button } from "@mui/material";
import type { Order } from "@orders/types/order";

const allowedExtensions = [".png", ".jpg", ".pdf"];

type FilePickerProps = {
  isDisabled: boolean;
  onSelect: (file: File, order: Order) => void;
  order: Order;
};

const FilePicker = ({ isDisabled, onSelect, order }: FilePickerProps) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const extension = "." + file.name.split(".").pop()?.toLowerCase();

    if (!allowedExtensions.includes(extension)) {
      alert("Only PNG, JPG and PDF files are allowed.");
      e.target.value = "";
      return;
    }

    onSelect(file, order);
  };

  return (
    <Button
      component="label"
      disabled={isDisabled}
      variant="contained"
      color="secondary"
    >
      {order.orderAttachment ? "Update Attachment" : "Add Attachment"}

      <input
        hidden={true}
        type="file"
        accept=".png,.jpg,.pdf"
        onChange={handleChange}
      />
    </Button>
  );
};

export default FilePicker;
