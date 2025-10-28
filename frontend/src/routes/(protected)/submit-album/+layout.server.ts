import { error } from "@sveltejs/kit";
import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async ({ locals }) => {
    const user = locals.user;
    console.log(user)
    if (!user.admin_rights) {
        error(403, { message: 'У вас нет доступа к этой странице.' })
    }
}