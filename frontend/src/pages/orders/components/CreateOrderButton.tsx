import { Button } from "@mui/material";
import { useContext } from "react";
import type { Dispatch, ReactElement, SetStateAction } from "react";

import { OrderRefreshContext } from "@orders/context/OrderRefreshContext";

import type { Item, ItemPost } from "@orders/types/item";
import type { Customer } from "@orders/types/order";

import { createOrder, createItem } from "@services/order";

const CreateOrderButton = ({
  customer,
  items,
  setSelectedCustomer,
  setSelectedItems,
}: Readonly<{
  customer: Customer;
  items: Item[];
  setSelectedCustomer: Dispatch<SetStateAction<Customer | undefined>>;
  setSelectedItems: Dispatch<SetStateAction<Item[]>>;
}>): ReactElement => {
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
};

export default CreateOrderButton;
