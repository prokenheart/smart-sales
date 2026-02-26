import { Button } from "@mui/material";
import type { Order } from "../types/order";

type FilePickerProps = {
  onSelect: (file: File, order: Order) => void;
  order: Order;
};

const FilePicker = ({ onSelect, order }: FilePickerProps) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onSelect(file, order);
    }
  };

  return (
    <Button component="label">
      {order.orderAttachment ? "Update Attachment" : "Add Attachment"}
      
      <input hidden={true} type="file" onChange={handleChange} />
    </Button>
  );
};

export default FilePicker;
