import { useInfiniteQuery, useQuery } from "@tanstack/react-query";
import { useMemo } from "react";

const API_BASE = "http://127.0.0.1:5000/api";

export interface Cuisine {
  id: number;
  name: string;
  total_orders: number;
  menu_count: number;
}

export interface Menu {
  id: number;
  name: string;
  price_per_person: number;
  min_spend: number;
  cuisines: { id: number; name: string }[];
  description: string;
  image: string;
}

interface PaginatedResponse {
  menus: Menu[];
  total: number;
  pages: number;
  current_page: number;
}

const fetchCuisines = async () => {
  const response = await fetch(`${API_BASE}/cuisines`);
  if (!response.ok) throw new Error("Failed to fetch cuisines");
  return response.json();
};

export function useMenuQueries(selectedCuisine: string | null) {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading: isLoadingMenus,
  } = useInfiniteQuery<PaginatedResponse>({
    queryKey: ["menus", selectedCuisine],
    queryFn: async ({ pageParam = 1 }) => {
      const url = selectedCuisine
        ? `${API_BASE}/menus/cuisine/${selectedCuisine}?page=${pageParam}`
        : `${API_BASE}/menus?page=${pageParam}`;

      const response = await fetch(url);
      if (!response.ok) throw new Error("Failed to fetch menus");
      return response.json();
    },
    getNextPageParam: (lastPage) => {
      if (lastPage.current_page < lastPage.pages) {
        return lastPage.current_page + 1;
      }
      return undefined;
    },
    initialPageParam: 1,
  });

  const cuisinesQuery = useQuery({
    queryKey: ["cuisines"],
    queryFn: fetchCuisines,
    staleTime: 1000 * 60 * 60,
  });

  const allMenus = data?.pages.flatMap((page) => page.menus) ?? [];

  return {
    menus: allMenus,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading: isLoadingMenus || cuisinesQuery.isLoading,
    cuisines: cuisinesQuery.data?.cuisines ?? [],
  };
}
