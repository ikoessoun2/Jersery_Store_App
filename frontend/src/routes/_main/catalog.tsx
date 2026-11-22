import { createFileRoute } from '@tanstack/react-router'
import CatalogPage from '@/pages/CatalogPage'

export const Route = createFileRoute('/_main/catalog')({
  component: CatalogPage,
})


