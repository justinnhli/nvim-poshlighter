if !exists('g:poshlighter_pos')
	let g:poshlighter_pos = ['verb']
endif

function! poshlighter#highlight()
	call call('POSHighlight', g:poshlighter_pos)
endfunction
