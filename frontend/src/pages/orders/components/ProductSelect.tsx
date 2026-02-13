import { Autocomplete, TextField } from "@mui/material";
import axios from "axios";
import { useEffect, useState, type Dispatch, type SetStateAction } from "react";
import type { Product } from "../types/product";

const API_URL = import.meta.env.VITE_API_URL;

export default function ProductSelect({
  selectedProduct,
  setSelectedProduct,
}: Readonly<{
  selectedProduct: Product | undefined;
  setSelectedProduct: Dispatch<SetStateAction<Product | undefined>>;
}>) {
  const [products, setProducts] = useState<Product[]>([]);

  const [keyword, setKeyword] = useState("");
  const [debouncedKeyword, setDebouncedKeyword] = useState("");

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedKeyword(keyword);
    }, 400);

    return () => clearTimeout(timer);
  }, [keyword]);


  useEffect(() => {
    if (!debouncedKeyword.trim()) {
      setProducts([]);
      return;
    }

    const fetchProducts = async () => {
      const res = await axios.get<Product[]>(
        `${API_URL}/products?query=${debouncedKeyword}`
      );

      setProducts(res.data);
    };

    fetchProducts();
  }, [debouncedKeyword]);
    
  return (
    <Autocomplete
      options={products}
      value={selectedProduct ?? null}
      onChange={(_, newValue) => setSelectedProduct(newValue ?? undefined)}
      getOptionLabel={(option) => option.productName}
      onInputChange={(_, value) => setKeyword(value)}
      renderOption={(props, option) => (
        <li {...props}>
          {option.productName} - {option.prices[0].priceAmount}
        </li>
      )}
      renderInput={(params) => (
        <TextField {...params} label="Select Product" size="small" />
      )}
      isOptionEqualToValue={(option, value) =>
        option.productId === value.productId
      }
    />
  );
}
