export function formatTimeAgo(dateString) {
    const date = new Date(dateString);
    
    if (isNaN(date.getTime())) {
        return null;
    }
    
    const now = new Date();
    const diffMs = now - date;
    const diffSecs = Math.floor(diffMs / 1000);

    if (diffSecs < 60) {
        return `${diffSecs} sekunder`;
    }

    const diffMins = Math.floor(diffSecs / 60);
    if (diffMins < 60) {
        return `${diffMins} minut${diffMins !== 1 ? 'ter' : ''}`;
    }

    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) {
        return `${diffHours} time${diffHours !== 1 ? 'r' : ''}`;
    }

    const diffDays = Math.floor(diffHours / 24);
    if (diffDays < 30) {
        const remainingHours = diffHours % 24;
        if (remainingHours > 0) {
            return `${diffDays} dag${diffDays !== 1 ? 'e' : ''} og ${remainingHours} time${remainingHours !== 1 ? 'r' : ''}`;
        }
        return `${diffDays} dag${diffDays !== 1 ? 'e' : ''}`;
    }

    const diffMonths = Math.floor(diffDays / 30);
    if (diffMonths < 12) {
        return `${diffMonths} måned${diffMonths !== 1 ? 'er' : ''}`;
    }

    const diffYears = Math.floor(diffMonths / 12);
    return `${diffYears} år`;
}


export function sortGroups(groups, sortBy = 'name') {
    const sortedKeys = Object.keys(groups).sort((a, b) => {
        if (sortBy === 'name') {
            if (a === 'Ukendt') return 1;
            if (b === 'Ukendt') return -1;
            return a.localeCompare(b);
        } else if (sortBy === 'count') {
            return groups[b].length - groups[a].length;
        }
        return 0;
    });

    const sortedGroups = {};
    sortedKeys.forEach(key => {
        sortedGroups[key] = groups[key];
    }
    );
    return sortedGroups;
}

export default { formatTimeAgo, sortGroups };
// Named exports are used above; no default export.