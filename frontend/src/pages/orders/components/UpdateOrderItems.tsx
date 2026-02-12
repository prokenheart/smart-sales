import { Button } from "@mui/material";
import type { Item } from "../types/item";
import axios from "axios";

export default function UpdateOrderItems({
  editItems,
}: Readonly<{ editItems: Item[] }>) {
  const handleSave = async () => {
    try {
      const res = await axios.put("https://your-api/orders/update-items", {
        items: editItems,
      });
			console.log(res.data);
    } catch (error) {
      console.error("UPDATE FAILED", error);
    }
  };

  return (
    <Button variant="contained" onClick={handleSave}>
      Save
    </Button>
  );
}
