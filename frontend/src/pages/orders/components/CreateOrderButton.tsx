import { Button } from "@mui/material";
import type { Item, ItemPost } from "../types/item";
import type { Customer } from "../types/order";
import { useContext, type Dispatch, type SetStateAction } from "react";
import { createOrder, createItem } from "../../../services/order";
import { OrderRefreshContext } from "../context/OrderRefreshContext";

export default function CreateOrderButton({
  customer,
  items,
  setSelectedCustomer,
  setSelectedItems,
}: Readonly<{
  customer: Customer;
  items: Item[];
  setSelectedCustomer: Dispatch<SetStateAction<Customer | undefined>>;
  setSelectedItems: Dispatch<SetStateAction<Item[]>>;
}>) {
  const refresh = useContext(OrderRefreshContext);

  const handleSave = async () => {
    let orderId;
    try {
      const res = await createOrder(customer.customerId);
      orderId = res.data.orderId;
    } catch (error) {
      console.error("UPDATE FAILED", error);
    }

    const itemPosts: ItemPost[] = items.map((item) => ({
      productId: item.product.productId,
      itemQuantity: item.itemQuantity,
    }));

    try {
      if (orderId != undefined) {
        const res = await createItem(orderId, itemPosts);
        if (res.status == 200) {
          setSelectedCustomer(undefined);
          setSelectedItems([]);
          refresh?.setShouldRefreshOrder(true);
        }
      }
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
