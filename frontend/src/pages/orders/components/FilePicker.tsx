import { Button } from "@mui/material";
import type { Order } from "@orders/types/order";

type FilePickerProps = {
  isDisabled: boolean;
  onSelect: (file: File, order: Order) => void;
  order: Order;
};

const FilePicker = ({ isDisabled, onSelect, order }: FilePickerProps) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onSelect(file, order);
    }
  };

  return (
    <Button component="label" disabled={isDisabled} variant="contained" color="secondary">
      {order.orderAttachment ? "Update Attachment" : "Add Attachment"}
      
      <input hidden={true} type="file" onChange={handleChange} />
    </Button>
  );
};

export default FilePicker;
