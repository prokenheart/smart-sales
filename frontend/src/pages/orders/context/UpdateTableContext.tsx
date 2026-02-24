import { createContext } from "react";
import type { Dispatch, SetStateAction } from "react";
import type { Order } from "../types/order";

export const UpdateTableContext = createContext<{
    setUpdatedOrder: Dispatch<SetStateAction<Order | undefined>>;
} | null>(null);
