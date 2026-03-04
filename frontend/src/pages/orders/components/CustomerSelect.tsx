import { Autocomplete, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import type { Dispatch, ReactElement, SetStateAction } from "react";

import type { Customer } from "@orders/types/order";

import { searchCustomers } from "@/services/customer";

const CustomerSelect = ({
  selectedCustomer,
  setSelectedCustomer,
}: Readonly<{
  selectedCustomer: Customer | undefined;
  setSelectedCustomer: Dispatch<SetStateAction<Customer | undefined>>;
}>): ReactElement => {
  const [customers, setCustomers] = useState<Customer[]>([]);

  const [keyword, setKeyword] = useState("");
  const [debouncedKeyword, setDebouncedKeyword] = useState("");

  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedKeyword(keyword);
    }, 400);

    return () => clearTimeout(timer);
  }, [keyword]);

  useEffect(() => {
    if (!debouncedKeyword.trim()) {
      setCustomers([]);
      return;
    }

    const fetchCustomers = async () => {
      try {
        setIsLoading(true);
        const res = await searchCustomers(debouncedKeyword);
        setCustomers(res.data);
      } finally {
        setIsLoading(false);
      }
    };

    fetchCustomers();
  }, [debouncedKeyword]);

  return (
    <Autocomplete
      options={customers}
      loading={isLoading}
      value={selectedCustomer ?? null}
      onChange={(_, newValue) => setSelectedCustomer(newValue ?? undefined)}
      getOptionLabel={(option) =>
        `${option.customerName} - ${option.customerPhone}`
      }
      onInputChange={(_, value) => setKeyword(value)}
      noOptionsText={
        keyword.trim() === "" ? "Type to search customer" : "No customers found"
      }
      loadingText="Finding customer..."
      renderInput={(params) => (
        <TextField {...params} label="Select Customer" size="small" />
      )}
      isOptionEqualToValue={(option, value) =>
        option.customerId === value.customerId
      }
      fullWidth
    />
  );
};

export default CustomerSelect;
