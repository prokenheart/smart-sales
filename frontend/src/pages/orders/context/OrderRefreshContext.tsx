import { createContext } from "react";
import type { Dispatch, SetStateAction } from "react";

export const OrderRefreshContext = createContext<{
	setShouldRefreshOrder: Dispatch<SetStateAction<boolean>>;
} | null>(null);
