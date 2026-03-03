import axios from "axios";

export const createS3Instance = (contentType: string) => {
  return axios.create({
    headers: {
      "Content-Type": contentType,
    },
  });
};