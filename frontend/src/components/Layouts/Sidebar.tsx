import {useState} from 'react';
import {SquareMenu, SquareX} from 'lucide-react'
type MenuItem = {
    label: string;
    link: string;
};

interface SidebarProps {
    menuItems: MenuItem[];
    isMobile?: boolean;
}

function SidebarMenus({menuItems} : SidebarProps){
    return(
        <div className='w-64 h-screen ease-in-out shrink-0 bg-slate-900'>
            {menuItems.map(item => (
                <a key={item.link} href={item.link} className="block px-4 py-2 hover:bg-slate-700 text-white text-center">
                    {item.label}
                </a>    
            ))}
        </div>
    )
}



export default function Sidebar({menuItems, isMobile} : SidebarProps){
    const [sidebarMenuButton, setSidebarMenuButton] = useState<boolean | undefined>(isMobile);
    const [sidebarOpen, setSidebarOpen] = useState<boolean>(!isMobile)
    const toggleSidebar = () => {
        setSidebarMenuButton(!sidebarMenuButton);
        setSidebarOpen(!sidebarOpen);
    }
    return(
        <aside className="bg-slate-900 h-fit ">
        {sidebarMenuButton ?
            <button className='w-fit float-right h-fit' onClick={toggleSidebar}><SquareMenu color='white' size={32}/></button> :
            <button className='w-fit float-right h-fit' onClick={toggleSidebar}><SquareX color='white' size={32}/></button>
        }
        {sidebarOpen &&
            <SidebarMenus menuItems={menuItems}/> 
        }
        </aside>
    )
}



