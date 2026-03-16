import { Box, Typography } from "@mui/material";
import type { ReactElement, ReactNode } from "react";
import { ResponsiveContainer } from "recharts";

type Props = {
  title: string;
  content?: string;
  chart?: ReactNode;
  chartHeight?: number;
};

const CustomCard = ({
  title,
  content,
  chart,
  chartHeight,
}: Readonly<Props>): ReactElement => {
  return (
    <Box
      flex={1}
      p={3}
      borderRadius={3}
      boxShadow={2}
      bgcolor="background.paper"
    >
      <Typography variant="h6">{title}</Typography>

      <Typography variant="h4" mt={1} mb={1}>
        {content}
      </Typography>

      <Box height={chartHeight ?? 90}>
        <ResponsiveContainer width="100%" height="100%">
          {chart}
        </ResponsiveContainer>
      </Box>
    </Box>
  );
};

export default CustomCard;
