import { Button, CircularProgress } from "@mui/material";
import { useContext, useState } from "react";
import type { Dispatch, ReactElement, SetStateAction } from "react";
import { HttpStatusCode } from "axios";

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
  const [isLoading, setIsLoading] = useState(false);

  const handleSave = async () => {
    setIsLoading(true);

    try {
      const orderRes = await createOrder(customer.customerId);
      const orderId = orderRes.data.orderId;

      const itemPosts: ItemPost[] = items.map((item) => ({
        productId: item.product.productId,
        itemQuantity: item.itemQuantity,
      }));

      const itemRes = await createItem(orderId, itemPosts);

      if (itemRes.status === HttpStatusCode.Ok) {
        setSelectedCustomer(undefined);
        setSelectedItems([]);
        refresh?.setShouldRefreshOrder(true);
      }
    } catch (error) {
      console.error("CREATE FAILED", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Button variant="contained" onClick={handleSave} disabled={isLoading}>
      {isLoading ? <CircularProgress size={20} /> : "Save"}
    </Button>
  );
};

export default CreateOrderButton;
