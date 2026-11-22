import { Button } from "@/components/ui/button"
import { Field } from "@/components/ui/field"
import { Input } from "@/components/ui/input"

type Category = {
  name : string;
  description : string;
  lastModified : string;
}



function InputInline() {
  return (
    <Field orientation="horizontal">
      <Input type="search" placeholder="Search..." />
      <Button>Search</Button>
    </Field>
  )
}


export default function CatalogPage() {
    return (
        <div className="flex-col">
            <div>
              <h1 className="text-center ">Welcome to the Catalog Page</h1>
              <h2> CATEGORY</h2>
            </div>
            <div>
                <InputInline/>
                <Button>New</Button>
            </div>
            <div>
              {/*Insert table for categories here */}
            </div>


        </div>

    )
}