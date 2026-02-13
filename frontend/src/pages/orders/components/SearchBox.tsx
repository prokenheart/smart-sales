import { TextField, InputAdornment, IconButton } from "@mui/material";
import { MdCancel } from "react-icons/md";
import { FaSearch } from "react-icons/fa";
import { useEffect, useState } from "react";

type SearchBoxProps = {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  delay?: number;
};

export default function SearchBox({
  value,
  onChange,
  placeholder = "Search Order...",
  delay = 400,
}: Readonly<SearchBoxProps>) {
  const [localValue, setLocalValue] = useState(value);

  useEffect(() => {
    setLocalValue(value);
  }, [value]);

  useEffect(() => {
    const timer = setTimeout(() => {
      onChange(localValue);
    }, delay);

    return () => clearTimeout(timer);
  }, [localValue, delay, onChange]);

  return (
    <TextField
      size="small"
      value={localValue}
      placeholder={placeholder}
      onChange={(e) => setLocalValue(e.target.value)}
      sx={{ width: 350 }}
      slotProps={{
        input: {
          startAdornment: (
            <InputAdornment position="start">
              <FaSearch size={14} />
            </InputAdornment>
          ),
          endAdornment: localValue ? (
            <InputAdornment position="end">
              <IconButton size="small" onClick={() => setLocalValue("")}>
                <MdCancel size={18} />
              </IconButton>
            </InputAdornment>
          ) : null,
        },
      }}
    />
  );
}
